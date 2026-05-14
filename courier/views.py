from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from admin_app.models import admin_dashboard_models
from courier.services import send_order_to_steadfast, refresh_consignment_status
from courier.steadfast import SteadfastCourier
import json

@staff_member_required
def send_to_steadfast_view(request, order_id):
    """Admin/staff triggers this to send a confirmed order to Steadfast."""
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)

    success, message, consignment = send_order_to_steadfast(order)

    if success:
        order.order_status = 'shipped'
        order.save()
        messages.success(request, f" Sent to Steadfast! Tracking: {consignment.tracking_code}")
    else:
        messages.error(request, f"Failed: {message}")

    return redirect(request.META.get('HTTP_REFERER', '/')) 

@staff_member_required
def track_order_view(request, order_id):
    """Refresh delivery status from Steadfast."""
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)
    success, message, consignment = refresh_consignment_status(order)

    if success:
        messages.success(request, f"Status: {consignment.status}")
    else:
        messages.error(request, message)

    return redirect(request.META.get('HTTP_REFERER', '/')) 


@staff_member_required
def courier_balance_view(request):
    """Check your Steadfast account balance."""
    courier = SteadfastCourier()
    response = courier.get_balance()
    return JsonResponse(response)




# Webhook — Steadfast calls this on status change

@csrf_exempt
@csrf_exempt
def steadfast_webhook(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    consignment_id = data.get("consignment_id")
    new_status     = data.get("status")

    if not consignment_id or not new_status:
        return JsonResponse({"error": "Missing data"}, status=400)

    consignment = admin_dashboard_models.SteadfastConsignment.objects.filter(
        consignment_id=str(consignment_id)
    ).select_related('order').first() 

    if not consignment:
        return JsonResponse({"error": "Consignment not found"}, status=404)


    consignment.status = new_status
    consignment.save()

    if new_status == 'delivered':
        consignment.order.order_status = 'delivered'
        consignment.order.save()
    elif new_status == 'cancelled':
        consignment.order.order_status = 'cancelled'
        consignment.order.save()

    return JsonResponse({"received": True, "status": new_status})