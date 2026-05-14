from datetime import date
from decimal import Decimal
from ..models import admin_dashboard_models

def coupon_discount_calculator(cart, coupon_obj):
    # Include number of use logic here.
    coupon_discount = 0
    if coupon_obj is not None:
        if cart.subtotal_after_discount >= coupon_obj.min_price:
            # if coupon_obj.type == 'product' and coupon_obj.start_date >= date.today() <= coupon_obj.end_date:
            if coupon_obj.type == 'product' and coupon_obj.start_date <= date.today() <= coupon_obj.end_date:
                if coupon_obj.is_percent:
                    coupon_discount = (cart.subtotal_after_discount * float(coupon_obj.value)) / 100
                    coupon_discount = (coupon_discount) if (cart.subtotal_after_discount - coupon_discount) > 0 else cart.subtotal_after_discount   #nja
                else:
                    coupon_discount = coupon_obj.value
                    coupon_discount = (coupon_discount) if (cart.subtotal_after_discount - coupon_discount) > 0 else cart.subtotal_after_discount   #nja
                    
            elif coupon_obj.type == 'delivery' and coupon_obj.start_date <= date.today() <= coupon_obj.end_date:
                delivery_data = cart.cart_delivery_charge
                if  delivery_data[0] == 0:
                    for item in delivery_data[1]:
                        if item['location'] == cart.delivery_location:
                            total_delivery_charge = item['total_delivery_charge']
                            break
                else:
                    total_delivery_charge = delivery_data[1]['total_delivery_charge']

                if coupon_obj.is_percent:
                    coupon_discount = (total_delivery_charge * float(coupon_obj.value)) / 100
                    # coupon_discount = (total_delivery_charge - coupon_discount) if (total_delivery_charge - coupon_discount) >= 0 else 0
                    coupon_discount = (coupon_discount) if (total_delivery_charge - coupon_discount) >= 0 else total_delivery_charge
                else:
                    coupon_discount = coupon_obj.value
                    coupon_discount = (coupon_discount) if (total_delivery_charge - coupon_discount) > 0 else total_delivery_charge

        return coupon_discount
    else:
        return coupon_discount


# cart session

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = admin_dashboard_models.Cart.objects.get_or_create(user=request.user)
        return cart
    
    if not request.session.session_key:
        request.session.create()
    cart, _ = admin_dashboard_models.Cart.objects.get_or_create(session_key=request.session.session_key)

    return cart