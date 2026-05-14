from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from accounts_app.models import User
from accounts_app.forms import UserForm, UserChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from io import BytesIO
from django.contrib import messages
from admin_app.models import admin_dashboard_models



def user_dashboard_views(request):
    cart_list = admin_dashboard_models.CartItem.objects.none()
    wish_list = admin_dashboard_models.Wishlist.objects.none()
    cart_total = 0
    recently_viewed_products = []
    if request.user.is_authenticated:
        recently_viewed_products = (
            admin_dashboard_models.RecentlyViewedProduct.objects.filter(user=request.user).prefetch_related('product__product_attribute', 'product__product_varient')[:6]
        )
        print("recently_viewed_products", recently_viewed_products)

        cart = admin_dashboard_models.Cart.objects.filter(user=request.user).first()

        if cart:
            cart_list = (
                admin_dashboard_models.CartItem.objects.filter(cart=cart)
                .select_related('product')
                .prefetch_related('product__product_varient', 'product__product_attribute')
            )
            

            cart_total = cart_list.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0

        wish_list = admin_dashboard_models.Wishlist.objects.filter(user=request.user)

    context = {
        'cart_list': cart_list,
        'wish_list': wish_list,
        'cart_total': cart_total,
        'recently_viewed_products': recently_viewed_products
    }
    return render(request, 'client/user_dashboard/dashboard.html', context)

@login_required
def user_profile_view(request):
    user = User.objects.get(email=request.user)
    return render(request, 'client/user_dashboard/profile.html', {"user": user})

@login_required
def user_profile_update_view(request):
    user = User.objects.get(email=request.user)
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User information updated succesfully!!!")
            return redirect("user_profile_view_url")
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'client/user_dashboard/profile_update.html', context)

@login_required
def user_change_password_view(request):
    user = request.user 

    if request.method == "POST":
        form = UserChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password updated successfully!")
            return redirect("user_profile_view_url")
        else:
            print(form.errors)
    else:
        form = UserChangePasswordForm(instance=user)

    context = {
        'form': form
    }
    return render(request, 'client/user_dashboard/change_password.html', context)

@login_required
def product_wishlist_view(request):
    if request.user.is_authenticated:
        wish_list = admin_dashboard_models.Wishlist.objects.filter(user=request.user).select_related('product').prefetch_related('product__product_attribute')
        user_wishlist_ids = admin_dashboard_models.Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        wish_list = admin_dashboard_models.Wishlist.objects.none()
        user_wishlist_ids = admin_dashboard_models.Wishlist.objects.none()
    context = {
        'wish_list': wish_list,
        'user_wishlist_ids': user_wishlist_ids
    }
    return render(request, 'client/user_dashboard/wishlist.html', context)

@login_required
def user_order_list_view(request, order_status=None):
    if request.user.is_authenticated:
        
        status_list = [
            ('all', 'All'),
            ('pending', 'Pending'), 
            ('confirmed', 'Confirmed'), 
            ('shipped', 'Shipped'), 
            ('delivered', 'Delivered'), 
            ('cancelled', 'Cancelled'), 
            ('returned', 'Returned')
        ]

        if order_status == None:
            orders = admin_dashboard_models.Order.objects.filter(user=request.user).order_by('-created_at')
        else:
            orders = admin_dashboard_models.Order.objects.filter(order_status=order_status, user = request.user).order_by('-created_at')

        context = {
            "orders": orders,
            "active_status": order_status,
            "status_list": status_list,
        }
    return render(request,'client/user_dashboard/order_history.html', context)

@login_required
def user_order_details_view(request, order_id):
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)
    product_item_obj = admin_dashboard_models.OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'product_item_obj': product_item_obj,
        "vat_gst": order.vat + order.gst

    }
    return render(request, 'client/user_dashboard/order_details.html', context)


def guest_user_order_details_view(request, order_id):
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)
    product_item_obj = admin_dashboard_models.OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'product_item_obj': product_item_obj,
        "vat_gst": order.vat + order.gst
    }
    return render(request, 'client/guest_user_order_details.html', context)




def download_order_details_pdf(request, order_id):
    order_items = admin_dashboard_models.OrderItem.objects.filter(order_id=order_id)
    order = order_items.first().order
    site_setting = admin_dashboard_models.SiteSetting.objects.first()

    context = {
        "order": order,
        "site_setting": site_setting,
        "order_items": order_items,
        "vat_gst": order.vat + order.gst,
        "user": request.user
    }

    template = get_template("client/user_dashboard/order_invoice_pdf.html")
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result)

    if pdf.err:
        return HttpResponse("Error generating PDF", status=400)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="order_{order.id}.pdf"'
    return response


@login_required
def download_order_invoice_view(request, order_id):
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)
    site_setting = admin_dashboard_models.SiteSetting.objects.first()
    order_items_obj = admin_dashboard_models.OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'site_setting': site_setting,
        'order_items': order_items_obj,
        'vat_gst': order.vat + order.gst,
        'user': request.user,
    }

    template = get_template("client/user_dashboard/invoice_download.html")
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result)

    if pdf.err:
        return HttpResponse("Error generating PDF", status=400)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Invoice_{order.id}.pdf"'
    return response
