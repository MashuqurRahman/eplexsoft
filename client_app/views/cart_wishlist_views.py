from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from django.db import transaction
from django.contrib import messages
from django.urls import reverse
from admin_app.views import global_function
import json
import uuid
from admin_app.models import admin_dashboard_models
from ..forms import client_forms
from ..views import calculation_views


def add_to_cart_view(request):
    if request.method == 'POST':
        attribute_id = request.POST.get('attribute_id')
        quantity     = request.POST.get('quantity')

        # ── Input validation ──
        if not attribute_id or not quantity:
            return JsonResponse({
                'success': False,
                'message': 'Missing required fields.'
            }, status=400)

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'message': 'Invalid quantity value.'
            }, status=400)

        # ── Get attribute ──
        try:
            product_attribute = admin_dashboard_models.ProductAttribute.objects.select_related(
                'product', 'color', 'size'
            ).get(id=attribute_id)
        except admin_dashboard_models.ProductAttribute.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product variant not found.'
            }, status=404)

        product = product_attribute.product
        moq = product.moq
        stock_status = product_attribute.attribute_stock_status
        remaining = stock_status['remaining_stock']

        if quantity < moq:
            return JsonResponse({
                'success': False,
                'message': f'Minimum order quantity is {moq}. '
                           f'Please enter at least {moq}.'
            }, status=400)

        if remaining <= 0:
            return JsonResponse({
                'success': False,
                'message': f'"{product.product_name}" is currently out of stock.'
            }, status=400)

        if quantity > remaining:
            return JsonResponse({
                'success': False,
                'message': f'Only {remaining} items available. You requested {quantity}.'
            }, status=400)

        # ── Duplicate check ──
        cart = global_function.get_or_create_cart(request)
        if admin_dashboard_models.CartItem.objects.filter(
            cart=cart,
            product=product,
            product_attribute=product_attribute
        ).exists():
            return JsonResponse({
                'success': False,
                'message': 'This product variant is already in your cart.'
            }, status=400)

        # ── Create cart item ──
        price = product_attribute.product_final_price
        admin_dashboard_models.CartItem.objects.create(
            cart=cart,
            product=product,
            product_attribute=product_attribute,
            quantity=quantity,
            price=price,
        )

        return JsonResponse({
            'success': True,
            'message': f'{product.product_name} added to cart successfully.',
            'cart_total': float(cart.subtotal_after_discount),
            'item_count': cart.items.count(),
            'product_name': product.product_name,
            'color': product_attribute.color.name if product_attribute.color else 'N/A',
            'size': product_attribute.size.value if product_attribute.size else 'N/A',
            'moq': moq,
            'stock': remaining,
        })

    return JsonResponse({'success': False,'message': 'Invalid request method.'}, status=405)


def delete_product_from_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')

        cart_item = get_object_or_404(admin_dashboard_models.CartItem, id=cart_item_id)

        cart = cart_item.cart
        cart.coupon = None
        cart.save()
        cart_item.delete()

        remaining_items = cart.items.all()
        item_count = remaining_items.count()

        cart_total = sum(item.price * item.quantity for item in remaining_items)
        
        return JsonResponse({
            'success': True,
            'cart_total': cart_total,
            'item_count': item_count,
            'is_empty': item_count == 0
        })

    return JsonResponse({'success': False}, status=400)

# PRODUCT ADD TO WISHLIST
def add_product_to_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = admin_dashboard_models.Product.objects.get(id=product_id)

        wishlist_item, created = admin_dashboard_models.Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})
    
    return JsonResponse({'error': "Invalid request"}, status=400)

# CHECKOUT
def update_cart_quantity(request):
    if request.method == "POST":
        cart_item_id = request.GET.get("cart_item_id")
        quantity = request.GET.get.data.get("quantity")
        

        cart_item = get_object_or_404(admin_dashboard_models.CartItem, id=cart_item_id)

        cart_item.quantity = quantity
        cart_item.save()

        cart = cart_item.cart

        return JsonResponse({
            "success": True,
            "cart_total": cart.total_price,
            "item_count": cart.items.count()
        })

    return JsonResponse({"success": False}, status=400)

# @transaction.atomic
# def product_checkout_view(request):
#     if request.user.is_authenticated:
#         cart = get_object_or_404(
#             admin_dashboard_models.Cart,
#             user=request.user
#         )
#         temp_user=request.user
#     else:
#         cart = admin_dashboard_models.Cart.objects.filter(session_key=request.session.session_key).first()
#         temp_user=None

    
#     cart_items = cart.items.select_related('product_attribute')
#     coupon_obj=None
#     shipping_method = None
#     if request.method == "POST":
#         shipping_method = request.POST.get('shipping_method')
#         coupon_id = request.POST.get('coupon_obj')

#         if coupon_id:
#             try:
#                 coupon_obj = admin_dashboard_models.CouponManagement.objects.get(id=int(coupon_id))
#             except admin_dashboard_models.CouponManagement.DoesNotExist:
#                 coupon_obj = None

#     totals = calculation_views.calculate_cart_totals(cart)
#     delivery_charge = calculation_views.calculate_delivery_charge(cart, 'inside_dhaka')
#     total_delivery_charge = delivery_charge['total_delivery_charge']
#     discount_price = calculation_views.calculate_delivery_discount(cart, total_delivery_charge)
#     vat_tax = calculation_views.vat_tax_calculation(cart)

    
#     form = client_forms.ShippingAddressForm(request.POST or None)
#     if request.method == 'POST':
#         form = client_forms.ShippingAddressForm(request.POST)
#         if form.is_valid():
#             instance = form.save()
            
#             order = admin_dashboard_models.Order.objects.create(
#                 user=temp_user,
#                 coupon=coupon_obj,
#                 order_no=str(uuid.uuid4()).replace('-', '')[:12],
#                 shipping_address=instance,
#                 total_amount=totals['total_payable'],
#                 shipping_charge=total_delivery_charge
#             )
#             for item in cart_items:
#                 admin_dashboard_models.OrderItem.objects.create(
#                 order=order,
#                 product=item.product_attribute.product,
#                 product_attribute=item.product_attribute,
#                 quantity=item.quantity,
#                 price=item.price,
#                 sub_total=item.subtotal,
#             )
            
#             cart.items.all().delete()

#             messages.success(request, "Order Placed Successfully!")
#             return redirect('product_checkout_url')
#         else:
#             messages.error(request, "Invalid form")

#     context = {
#         'form': form,
#         'cart_items': cart_items,
#         'sub_total': totals['subtotal'],
#         'vat': vat_tax['total_vat'],
#         'gst': vat_tax['total_gst'],
#         'discount': discount_price['total_discount'],
#         'sub_total_after_discount': totals['subtotal'] - discount_price['total_discount'],
#         'shipping': total_delivery_charge,
#         'total_tax_amount': vat_tax['total_tax_amount'],
#         'total_payable_amount': totals['subtotal'] - discount_price['total_discount'] - total_delivery_charge - vat_tax['total_tax_amount'],
#         'total_payable': totals['subtotal'] - discount_price['total_discount'] - vat_tax['total_tax_amount'] 
#     }
#     return render(request, 'client/products/checkout.html', context)

@transaction.atomic
def product_checkout_view(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(admin_dashboard_models.Cart, user=request.user)
        temp_user = request.user
    else:
        cart = admin_dashboard_models.Cart.objects.filter(session_key=request.session.session_key).first()
        temp_user = None

    cart_items = admin_dashboard_models.CartItem.objects.filter(cart = cart)
    
    coupon_obj = None
    coupon_discount = Decimal('0.00')
    
    coupon_id = request.POST.get('coupon_obj')
    if coupon_id:
        try:
            coupon_obj = admin_dashboard_models.CouponManagement.objects.get(id=int(coupon_id))
        except admin_dashboard_models.CouponManagement.DoesNotExist:
            coupon_obj = None

    # cart_item = admin_dashboard_models.CartItem.objects.get(cart_id=cart.id)
    # subtotal = cart_item.product_attribute.

    
    form = client_forms.ShippingAddressForm(request.POST or None)
    out_of_stock = False
    
    for item in cart_items:
        if not item.product_attribute.attribute_stock_status["status"]:
            out_of_stock = True
           
    
    if request.method == 'POST':
        form = client_forms.ShippingAddressForm(request.POST)
        payment_method = request.POST.get('payment_method')
        if form.is_valid():
            shipping_instance = form.save()
            coupon_code = request.POST.get('coupon_code')
            if coupon_code:
                try:
                    coupon_obj = admin_dashboard_models.CouponManagement.objects.get(code=coupon_code)
                except admin_dashboard_models.CouponManagement.DoesNotExist:
                    coupon_obj = None
       
            order = admin_dashboard_models.Order.objects.create(
                user=temp_user,
                coupon=coupon_obj,
                order_no=str(uuid.uuid4()).replace('-', '')[:12],
                shipping_address=shipping_instance,
                total_payable=cart.total_payable["total_payable_amount"],
                shipping_charge=cart.total_payable["total_delivery_charge"],
                sub_total = cart.subtotal,
                sub_total_after_discount = cart.subtotal_after_discount,
                discount = cart.cart_discount,
                shipping_method = cart.delivery_location,
                payment_method = payment_method,
                vat = cart.vat_gst_amount["total_vat"],
                gst = cart.vat_gst_amount["total_gst"],
                coupon_price = cart.vat_gst_amount["coupon_discount_price"]
                
            )

            for item in cart_items:
                admin_dashboard_models.OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_attribute=item.product_attribute,
                    quantity=item.quantity,
                    price=item.product_attribute.product_final_price
                    
                )
                
                item.delete()
                

            cart.delete()

            messages.success(request, "Order Placed Successfully!")
            if not request.user.is_authenticated:
                return redirect('guest_user_order_detail_url', order_id=order.id)
            return redirect('home_page_url')
        else:
            messages.error(request, "Invalid form submission!")

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        # 'sub_total': totals['subtotal'],
        # 'discount': discount_price,
        # 'sub_total_after_discount': float(totals['subtotal']) - discount_price,
        # 'shipping': adjusted_delivery_charge,
        'coupon_obj': coupon_obj.id if coupon_obj else None,
        'coupon_discount': coupon_discount,
        'total_payable': cart.total_payable['total_payable_amount'],
        'total_delivery_charge': cart.total_payable['total_delivery_charge'],
        'out_of_stock':out_of_stock
    }

    return render(request, 'client/products/checkout.html', context)



def buy_now_products_view(request, attribute_id):
    product_attributes_obj = admin_dashboard_models.ProductAttribute.objects.select_related(
        'product', 'color', 'size'
    ).filter(id=attribute_id).first()

    if not product_attributes_obj:
        messages.error(request, 'Product variant not found.')
        return redirect('home')

    product = product_attributes_obj.product
    moq = product.moq
    stock_status = product_attributes_obj.attribute_stock_status
    remaining = stock_status['remaining_stock']

    from django.urls import reverse
    try:
        product_page_url = reverse(
            'product_details_page_url',
            args=[product.id]
        )
    except Exception:
        product_page_url = request.META.get('HTTP_REFERER', '/')

    qty = request.GET.get('qty')
    try:
        qty = int(qty) if qty else moq
    except (ValueError, TypeError):
        qty = moq

    if qty < moq:
        messages.error(
            request,
            f'Minimum order quantity is {moq}. Please enter at least {moq}.'
        )
        return redirect(product_page_url)

    if remaining <= 0:
        messages.error(
            request,
            f'"{product.product_name}" is currently out of stock.'
        )
        return redirect(product_page_url)

    if qty > remaining:
        messages.error(
            request,
            f'Only {remaining} items available. You requested {qty}.'
        )
        return redirect(product_page_url)

    if request.user.is_authenticated:
        cart, created = admin_dashboard_models.Cart.objects.get_or_create(
            user=request.user
        )
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = admin_dashboard_models.Cart.objects.get_or_create(
            session_key=request.session.session_key
        )

    price = product_attributes_obj.product_final_price

    # ── Duplicate check ──
    if admin_dashboard_models.CartItem.objects.filter(
        cart=cart,
        product=product,
        product_attribute=product_attributes_obj
    ).exists():
        messages.warning(request, 'This product variant is already in your cart.')
        return redirect('product_checkout_url')

    # ── Create cart item ──
    admin_dashboard_models.CartItem.objects.create(
        cart=cart,
        product=product,
        product_attribute=product_attributes_obj,
        quantity=qty,
        price=price,
    )

    return redirect('product_checkout_url')