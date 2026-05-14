import math
from decimal import Decimal
from admin_app.models import admin_dashboard_models

#Checkout calculation
def calculate_cart_totals(cart):
    subtotal = cart.subtotal

    discount = Decimal('0.00')

    vat = subtotal * Decimal('0.02')
    gst = subtotal * Decimal('0.03')
    total_tax = vat + gst

    total_payable = subtotal - discount + total_tax

    return {
        'subtotal': subtotal,
        'discount': discount,
        'vat': vat,
        'gst': gst,
        'tax': total_tax,
        'total_payable': total_payable
    }


def calculate_delivery_charge(cart, location):
    total_delivery_charge = Decimal('0.00')

    for item in cart.items.select_related('product', 'product_attribute', 'product__sub_sub_categories'):
        product_weight = Decimal(item.product_attribute.weight or 0)

        delivery_charge_obj = admin_dashboard_models.SubSubCategoryDeliveryCharge.objects.select_related(
            'delivery_charge'
        ).filter(
            sub_sub_category=item.product.sub_sub_categories,
            delivery_charge__delivery_location=location
        ).first()

        if not delivery_charge_obj:
            continue

        dc = delivery_charge_obj.delivery_charge
        initial_weight = Decimal(dc.initial_weight)
        initial_charge = Decimal(dc.initial_charge)
        increment_weight = Decimal(dc.increment_weight_per_unit)

        charge = initial_charge

        if product_weight > initial_weight:
            extra_weight = product_weight - initial_weight

            extra_charge = math.ceil(extra_weight * increment_weight)

            charge += extra_charge

        total_delivery_charge += charge

    return {
        'total_delivery_charge': total_delivery_charge
    }


def calculate_delivery_discount(cart, total_delivery_charge):
    return {
        'total_discount': cart.cart_delivery_charge[1]['discount_price'] if cart.cart_delivery_charge[0] else 0
    }

        