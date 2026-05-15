import json
from decimal import Decimal
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from admin_app.models import admin_dashboard_models
from client_app.views import calculation_views
from ..views import global_function
from django.shortcuts import render, redirect, get_object_or_404

def load_sub_category(request):
    category_id = request.GET.get('category')
    category_obj = admin_dashboard_models.SubCategories.objects.filter(categories__id=category_id).order_by('-id')
    return render(request, 'custom-admin/ajax_load/load_category.html', {'category_obj': category_obj})


def load_sub_category_based_on_sub_sub_category(request):
    category_id = request.GET.get('category')
    category_obj = admin_dashboard_models.SubCategories.objects.filter(categories__id=category_id, has_sub_sub_cat=True).order_by('-id')
    return render(request, 'custom-admin/ajax_load/load_category.html', {'category_obj': category_obj})

def load_sub_sub_category(request):
    category_id = request.GET.get('sub_category')
    category_obj = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__id=category_id).order_by('-id')
    return render(request, 'custom-admin/ajax_load/load_sub_category.html', {'category_obj': category_obj})

def ajax_load_products(request):
    sub_sub_cat_id = request.GET.get('sub_sub_catId')
    product_obj = admin_dashboard_models.Product.objects.filter(sub_sub_categories__id=sub_sub_cat_id).order_by('-id')
    return render(request, 'custom-admin/ajax_load/load_products.html', {'product_obj': product_obj})

def load_sub_sub_category_from_category(request):
    category_id = request.GET.get('category')
    category_obj = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories__id=category_id).order_by('-id')
    return render(request, 'custom-admin/ajax_load/load_sub_sub_category.html', {'category_obj': category_obj})


# APPLY COUPON
# @csrf_exempt
# def apply_coupon(request):
#     # try:
#         data = json.loads(request.body)
#         coupon_code = data.get("coupon_code")
#         shipping_method = data.get("shipping_method")

#         qty = data.get("quantity")
        
#         if request.user.is_authenticated:
#             cart = get_object_or_404(admin_dashboard_models.Cart, user=request.user)
#         else:
#             cart = get_object_or_404(admin_dashboard_models.Cart, session_key=request.session.session_key)



#         if not shipping_method:
#             return JsonResponse({'success': False, 'message': 'Shipping method is required'}, status=400)

#         cart.delivery_location = shipping_method
#         cart.save()


#         try:
#             coupon_obj = admin_dashboard_models.CouponManagement.objects.get(code=coupon_code)
#             coupon_usage_count = admin_dashboard_models.Order.objects.filter(coupon=coupon_obj).count()

#             if coupon_usage_count >= coupon_obj.number_of_user:
#                 return JsonResponse({'success': False, 'message': 'This coupon is out of limit'}, status=400)
            
#             if cart.coupon and cart.coupon.id == coupon_obj.id:
#                 return JsonResponse({'success': False, 'message': 'This coupon is already applied!'}, status=400) 
              
#             if (date.today() < coupon_obj.start_date):
#                 return JsonResponse({'success': False, 'message': 'Coupon is not active yet!'})
            
#             if (date.today() > coupon_obj.end_date):
#                 return JsonResponse({'success': False, 'message': 'Coupon Expired!'})
            
#             if coupon_obj.min_price > cart.subtotal_after_discount:
#                 return JsonResponse({'success': False, 'message': 'Coupon value does not meet minimum price.'})
    
            
#         except:
#             pass
         
#         coupon_obj = admin_dashboard_models.CouponManagement.objects.filter(code=coupon_code).first()

#         if not coupon_obj:
#             return JsonResponse({'success': False, 'message': 'Invalid Coupon!'}, status=400)
        
#         if coupon_obj:
#             coupon_usage_count = admin_dashboard_models.Order.objects.filter(coupon=coupon_obj).count()

#             if coupon_usage_count >= coupon_obj.number_of_user:
#                 return JsonResponse({'success': False, 'message': 'This coupon is out of limit'}, status=400)

#             cart.coupon = coupon_obj
#             cart.save()
#         else:
#             cart.coupon = None
#             cart.save()



#         coupon_discount_price = global_function.coupon_discount_calculator(cart, coupon_obj)

#         delivery_data = cart.cart_delivery_charge

#         if  delivery_data[0] == 0:
#             for item in delivery_data[1]:
#                 if item['location'] == shipping_method:
#                     total_delivery_charge = item['total_delivery_charge']
#                     break
#         else:
#             total_delivery_charge = delivery_data[1]['total_delivery_charge']

#         total_after_coupon = float(cart.subtotal_after_discount )+ float(total_delivery_charge) + float(cart.vat_gst_amount['total_tax_amount']) - float(coupon_discount_price)

#         return JsonResponse({
#             'success': True,
#             'coupon_id': coupon_obj.id if coupon_obj else False,
#             'total_delivery_charge': str(total_delivery_charge),
#             'coupon_discount': float(coupon_discount_price),
#             'total_after_coupon': float(total_after_coupon),
#             'message': 'Coupon applied successfully'
#         })

#     # except Exception as e:
#     #     return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
def apply_coupon(request):
    data = json.loads(request.body)
    coupon_code = data.get("coupon_code")
    shipping_method = data.get("shipping_method")

    if request.user.is_authenticated:
        cart = get_object_or_404(
            admin_dashboard_models.Cart,
            user=request.user
        )
    else:
        cart = get_object_or_404(
            admin_dashboard_models.Cart,
            session_key=request.session.session_key
        )

    if not shipping_method:
        return JsonResponse({
            'success': False,
            'message': 'Shipping method is required'
        }, status=400)

    cart.delivery_location = shipping_method
    cart.save()

    if not coupon_code or coupon_code.strip() == "":
        cart.coupon = None
        cart.save()

        coupon_discount_price = Decimal("0.00")
        total_delivery_charge = cart.total_payable['total_delivery_charge']
        total_after_coupon = cart.total_payable['total_payable_amount']
        vat_gst = cart.vat_gst_amount 

        return JsonResponse({
            'success': True,
            'coupon_id': False,
            'total_delivery_charge': str(total_delivery_charge),
            'coupon_discount': 0,
            'total_after_coupon': float(total_after_coupon),
            'total_vat': float(vat_gst['total_vat']),
            'total_gst': float(vat_gst['total_gst']), 
            'total_tax_amount': float(vat_gst['total_tax_amount']), 
            'message': ''
        })
    
    try:
        coupon_obj = admin_dashboard_models.CouponManagement.objects.get(
            code=coupon_code
        )
    except admin_dashboard_models.CouponManagement.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Invalid Coupon!'
        }, status=400)

    today = date.today()


    if coupon_obj.start_date and today < coupon_obj.start_date:
        return JsonResponse({
            'success': False,
            'message': 'Coupon is not active yet!'
        }, status=400)

    if coupon_obj.end_date and today > coupon_obj.end_date:
        return JsonResponse({
            'success': False,
            'message': 'Coupon Expired!'
        }, status=400)

    coupon_usage_count = admin_dashboard_models.Order.objects.filter(
        coupon=coupon_obj
    ).count()

    if coupon_obj.number_of_user and coupon_usage_count >= coupon_obj.number_of_user:
        return JsonResponse({
            'success': False,
            'message': 'This coupon is out of limit'
        }, status=400)

 
    if cart.coupon and cart.coupon.id == coupon_obj.id:
        return JsonResponse({
            'success': False,
            'message': 'This coupon is already applied!'
        }, status=400)

    if coupon_obj.min_price and cart.subtotal_after_discount < coupon_obj.min_price:
        return JsonResponse({
            'success': False,
            'message': 'Coupon value does not meet minimum price.'
        }, status=400)

    cart.coupon = coupon_obj
    cart.save()

    coupon_discount_price = global_function.coupon_discount_calculator(
        cart,
        coupon_obj
    )

    delivery_data = cart.cart_delivery_charge or [0, []]
    total_delivery_charge = Decimal("0.00")

    if delivery_data[0] == 0:
        for item in delivery_data[1]:
            if item['location'] == shipping_method:
                total_delivery_charge = Decimal(item['total_delivery_charge'])
                break
    else:
        total_delivery_charge = Decimal(delivery_data[1]['total_delivery_charge'])

    # total_vat, total_gst, applicable_amount = 0, 0, 0
    total_vat = Decimal("0.00")
    total_gst = Decimal("0.00")
    
    cart_items = admin_dashboard_models.CartItem.objects.filter(cart=cart)
    
    for item in cart_items:

        item_total = Decimal(item.cart_item_total_price)
        vat_rate = Decimal(item.product.vat_tax_amount or 0)
        gst_rate = Decimal(item.product.gst_amount)
        is_percent = item.product.is_applicable

        base_amount = item_total

        if cart.coupon and cart.coupon.type == "product":
            # base_amount = item_total - Decimal(coupon_discount_price)
            base_amount = item_total

        # Prevent negative
        base_amount = max(base_amount, Decimal('0'))
        if is_percent:
            vat = (base_amount * vat_rate) / Decimal('100')
            gst = (base_amount * gst_rate) / Decimal('100')
        else:
            if base_amount<=0:
                vat = 0
                gst = 0
            else:
                vat = vat_rate * item.quantity
                gst = gst_rate * item.quantity

        total_vat += vat
        total_gst += gst

    total_after_coupon = (
        Decimal(cart.subtotal_after_discount)
        + total_delivery_charge
        + Decimal(cart.vat_gst_amount.get('total_tax_amount', 0) or 0)
        - Decimal(coupon_discount_price)
    )

    return JsonResponse({
        'success': True,
        'coupon_id': coupon_obj.id,
        'total_delivery_charge': str(total_delivery_charge),
        'coupon_discount': float(coupon_discount_price),
        'total_after_coupon': float(total_after_coupon),
        'total_vat': float(total_vat),
        'total_gst': float(total_gst),
        'total_tax_amount': float(total_vat) + float(total_gst),
        'message': 'Coupon applied successfully'
    })

def ajax_load_product_table(request):
    category_id = request.GET.get('category_id')
    campaign_id = request.GET.get('campaignID')
    campaign_product_list = admin_dashboard_models.FlashSell.objects.filter(side_slider__id=campaign_id).values_list('product', flat=True)
    obj_list = admin_dashboard_models.Product.objects.filter(categories_id=category_id, is_active=True).exclude(id__in=list(campaign_product_list))
    context = {
        'obj_list': obj_list
    }
    return render(request, 'custom-admin/flash_sell/product_table.html', context)


def ajax_update_cart_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart_item_id = data.get("cartItemId")
        quantity = data.get('quantity')

        cart_item_obj = admin_dashboard_models.CartItem.objects.get(id=cart_item_id)
        if quantity < cart_item_obj.product.moq:
            return JsonResponse({
            "success": False,
            "message": "Quantity cannot be less than MOQ"
        })

        if quantity >cart_item_obj.product_attribute.attribute_stock_status['remaining_stock']:
             return JsonResponse({
            "success": False,
            "message": "Quantity cannot be greater than stock limit"
        })

        cart_item_obj.quantity = quantity
        cart_item_obj.save()

    
        cart = cart_item_obj.cart
        coupon_discount_price = global_function.coupon_discount_calculator(
            cart,
            cart.coupon
        )
        total_vat, total_gst, applicable_amount = 0, 0, 0
    
        cart_items = admin_dashboard_models.CartItem.objects.filter(cart=cart)
        
        for item in cart_items:

            item_total = Decimal(item.cart_item_total_price)
            vat_rate = Decimal(item.product.vat_tax_amount)
            gst_rate = Decimal(item.product.gst_amount)
            is_percent = item.product.is_applicable

            base_amount = item_total
            if cart.coupon and cart.coupon.type == "product":
                # base_amount = item_total - Decimal(coupon_discount_price)
                base_amount = item_total

            # Prevent negative
            base_amount = max(base_amount, Decimal('0'))
            if is_percent:
                vat = (base_amount * vat_rate) / Decimal('100')
                gst = (base_amount * gst_rate) / Decimal('100')
            else:
                if base_amount<=0:
                    vat = 0
                    gst = 0
                else:
                    vat = vat_rate * item.quantity
                    gst = gst_rate * item.quantity

            total_vat += vat
            total_gst += gst

        return JsonResponse({
            "success": True,
            'cart_item_total_price': cart_item_obj.cart_item_total_price,
            'total_payable': cart.total_payable['total_payable_amount'],
            'counter': cart_item_obj.quantity,
            'cart_item_unit_price': cart_item_obj.product_attribute.product_final_price,
            'subtotal':cart.subtotal,
            'discount':cart.cart_discount,
            'total_vat': float(total_vat),
            'total_gst': float(total_gst),
            'total_tax_amount': float(total_vat) + float(total_gst),
            'subtotal_after_discount':cart.subtotal_after_discount,
            'stock_qty':cart_item_obj.product_attribute.attribute_stock_status['remaining_stock']

            # "total": total
        })