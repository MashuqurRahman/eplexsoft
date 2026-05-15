import requests
from django.contrib.auth.decorators import login_required
from .steadfast import SteadfastCourier
from .pathao import PathaoCourier
from .redx import RedXCourier
from admin_app.models import admin_dashboard_models

@login_required
def send_order_to_steadfast(order):
    shipping = order.shipping_address
    recipient_name = f"{shipping.full_name}"
    recipient_phone = shipping.phone_no
    recipient_address = (
        f"{shipping.address_line}, {shipping.thana}, {shipping.upozila}, {shipping.city}, {shipping.postal_code}"
        if hasattr(shipping, 'city') else shipping.address_line
    )
    cod_amount = order.total_payable

    try:
        courier = SteadfastCourier()
    except Exception as e:
        return False, str(e), None

    try:
        response = courier.place_order(
            invoice=order.order_no,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            recipient_address=recipient_address,
            cod_amount=cod_amount,
            note=f"Products: {order.order_wise_products}",
        )
    except Exception as e:
        return False, f"Request failed: {str(e)}", None
    

    if response.get("status") == 200:
        consignment_data = response.get("consignment", {})

        consignment_obj, created = admin_dashboard_models.SteadfastConsignment.objects.update_or_create(
            order=order,
            defaults={
                "consignment_id": consignment_data.get("consignment_id"),
                "tracking_code": consignment_data.get("tracking_code"),
                "invoice": consignment_data.get("invoice"),
                "recipient_name": consignment_data.get("recipient_name"),
                "recipient_phone": consignment_data.get("recipient_phone"),
                "recipient_address": consignment_data.get("recipient_address"),
                "cod_amount": consignment_data.get("cod_amount"),
                "status": consignment_data.get("status", "pending"),
                "raw_response": response,
            }
        )
        if consignment_obj:
            order.order_status = 'shipped'
            order.save(update_fields=['order_status'])

        return True, "Consignment created successfully.", consignment_obj

    return False, response.get("message", "Unknown error from Steadfast."), None


@login_required
def refresh_consignment_status(order):
    consignment = admin_dashboard_models.SteadfastConsignment.objects.filter(order=order).first()

    if not consignment:
        return False, "No consignment found for this order.", None

    try:
        courier = SteadfastCourier() 
    except Exception as e:
        return False, str(e), None
    
    try:
        response = courier.check_status_by_consignment_id(consignment.consignment_id)
    except Exception as e:
        return False, f"Request failed: {str(e)}", None

    delivery_status = response.get("delivery_status")

    if delivery_status:
        delivery_status = delivery_status.lower().strip()

    if not delivery_status or delivery_status in ['unknown', 'not_found', 'not found']:
        order.order_status = 'confirmed'
        order.save(update_fields=['order_status'])

        consignment.delete()
        return True, "Consignment is deleted", None


    consignment.status = delivery_status
    consignment.raw_response = response
    consignment.save()

    if delivery_status == 'delivered':
        order.order_status = 'delivered'
    elif delivery_status == 'cancelled':
        order.order_status = 'cancelled'
    elif delivery_status == 'returned':
        order.order_status = 'returned'

    order.save(update_fields=['order_status'])

    return True, "Status updated.", consignment



# PATHAO START

@login_required
def send_order_to_pathao(order):
    shipping = order.shipping_address
    recipient_name = shipping.full_name
    recipient_phone = shipping.phone_no
    recipient_address = (
        f"{shipping.address_line}, {shipping.thana}, {shipping.upozila}, {shipping.city}, {shipping.postal_code}"
        if hasattr(shipping, 'city') else shipping.address_line
    )
    cod_amount = order.total_payable

    try:
        courier = PathaoCourier()
    except Exception as e:
        return False, str(e), None
    try:
        response = courier.place_order(
            merchant_order_id = order.order_no,
            recipient_name = recipient_name,
            recipient_phone = recipient_phone,
            recipient_address = recipient_address,
            cod_amount = cod_amount,
            item_description = f"Products: {order.order_wise_products}",
        )
    except Exception as e:
        return False, f"Request failed: {str(e)}", None
        
    if response.get("type") == "success" and response.get("code") == 200:
        consignment_data = response.get("data", {})

        consignment_obj, created = admin_dashboard_models.PathaoConsignment.objects.update_or_create(
            order=order,
            defaults={
                "consignment_id": consignment_data.get("consignment_id"),
                "merchant_order_id": consignment_data.get("merchant_order_id", order.order_no),
                "recipient_name": consignment_data.get("recipient_name"),
                "recipient_phone": consignment_data.get("recipient_phone"),
                "recipient_address": consignment_data.get("recipient_address"),
                "recipient_city": consignment_data.get("recipient_city"),
                "recipient_zone": consignment_data.get("recipient_zone"),
                "cod_amount": consignment_data.get("amount_to_collect"),
                "delivery_type": consignment_data.get("delivery_type"),
                "item_type": consignment_data.get("item_type"),
                "status": consignment_data.get("order_status", "pending").lower(),
                "raw_response": response,
            },
        )
        return True, "Consignment created successfully.", consignment_obj

    return False, response.get("message", "Unknown error from Pathao."), None

@login_required
def send_order_to_redx(order):
    shipping = order.shipping_address

    recipient_name = shipping.full_name
    recipient_phone = shipping.phone_no

    recipient_address = (
        f"{shipping.address_line}, {shipping.thana}, {shipping.upozila}, {shipping.city}, {shipping.postal_code}"
        if hasattr(shipping, 'city') else shipping.address_line
    )

    cod_amount = order.total_payable

    # ⚠️ You MUST already have these saved
    # delivery_area_id = getattr(order, "delivery_area_id", None)
    # delivery_area_name = getattr(order, "delivery_area_name", None)
    # print("delivery_area_id", delivery_area_id)

    # if not delivery_area_id:
    #     return False, "Missing delivery_area_id for RedX", None

    try:
        courier = RedXCourier()
    except Exception as e:
        return False, str(e), None

    try:
        response = courier.create_parcel(
            customer_name=recipient_name,
            customer_phone=recipient_phone,
            delivery_area='Dhaka',
            delivery_area_id=1,
            customer_address=recipient_address,
            cod_amount=cod_amount,
            weight=500,  # ⚠️ You can make dynamic
            merchant_invoice_id=order.order_no,
            instruction=f"Products: {order.order_wise_products}",
        )
    except Exception as e:
        return False, f"Request failed: {str(e)}", None

    tracking_id = response.get("tracking_id")
    print("response", response)
    if tracking_id:
        consignment_obj, created = admin_dashboard_models.RedXConsignment.objects.update_or_create(
            order=order,
            defaults={
                "tracking_id": tracking_id,
                "merchant_invoice_id": order.order_no,
                "recipient_name": recipient_name,
                "recipient_phone": recipient_phone,
                "recipient_address": recipient_address,
                "delivery_area": 'test',
                "delivery_area_id": 1,
                "cod_amount": cod_amount,
                "status": "pickup-pending",  # default RedX status
                "raw_response": response,
            },
        )

        return True, "Parcel created successfully.", consignment_obj

    return False, response, None
    



