import json
from decimal import Decimal
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_app.models import admin_dashboard_models
from client_app.models import client_models

@login_required
def order_list(request, order_status=None):
    status_list = [
        ('all', 'All'),
        ('pending', 'Pending'), 
        ('confirmed', 'Confirmed'), 
        ('shipped', 'Shipped'), 
        ('delivered', 'Delivered'), 
        ('cancelled', 'Cancelled'), 
        ('returned', 'Returned')
    ]
    orders = []
    if request.user.is_superuser or request.user.role == 'central_admin':
        if order_status is None:
            orders = admin_dashboard_models.Order.objects.all().order_by('-created_at')
        else:
            orders = admin_dashboard_models.Order.objects.filter(order_status=order_status).order_by('-created_at')
    else:
        return render(request, 'permission_denied.html')

    for order in orders:
        consignment = admin_dashboard_models.SteadfastConsignment.objects.filter(order=order).first()
        order.consignment_obj = consignment 

    context = {
        "orders": orders,
        "active_status": order_status,
        "status_list": status_list,
    }
    return render(request, "custom-admin/orders/order_list.html", context)


def order_edit_view(request, order_id):
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)
    order_items = admin_dashboard_models.OrderItem.objects.filter(order=order).select_related(
        'product', 'product_attribute', 'product_attribute__color', 'product_attribute__size'
    )

    products = admin_dashboard_models.Product.objects.prefetch_related(
        'product_attribute', 'product_categories'
    ).all()

    categories = admin_dashboard_models.Categories.objects.all()

    delivery_charges = admin_dashboard_models.DeliveryCharge.objects.filter(is_active=True)
    delivery_charge_data = {}
    for charge in delivery_charges:
        delivery_charge_data[charge.delivery_location] = {
            'initial_charge': charge.initial_charge,
            'initial_weight': charge.initial_weight,
            'increment_weight_per_unit': charge.increment_weight_per_unit,
        }

    context = {
        'order': order,
        'order_items': order_items,
        'product_item_obj': order_items,
        'products': products,
        'categories': categories,
        'vat_gst': (order.vat or 0) + (order.gst or 0),
        'delivery_charge_data': delivery_charge_data,
    }
    return render(request, 'custom-admin/orders/order_edit.html', context)

@login_required
def get_product_variants_ajax(request):
    product_id = request.GET.get('product_id', '').strip()

    if not product_id:
        return JsonResponse({'variants': []})

    try:
        product_id = int(product_id)
    except ValueError:
        return JsonResponse({'variants': []})

    try:
        attrs = admin_dashboard_models.ProductAttribute.objects.select_related(
            'color', 'size'
        ).filter(product_id=product_id)

        variants = []
        for attr in attrs:
            try:
                stock = attr.attribute_stock_status
                variants.append({
                    'product_attribute_id': attr.id,
                    'size':     str(attr.size)  if attr.size  else 'N/A',
                    'color':    str(attr.color) if attr.color else 'N/A',
                    'price':    float(attr.product_final_price),
                    'stock':    stock['remaining_stock'],
                    'in_stock': stock['status'],
                })
            except Exception as attr_err:
                continue

        return JsonResponse({'variants': variants})

    except Exception as e:
        return JsonResponse({'error': str(e), 'variants': []}, status=400)


@login_required
@require_POST
def update_shipping_address_ajax(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        order = get_object_or_404(admin_dashboard_models.Order, id=order_id)
        address = order.shipping_address

        address.full_name = data.get('full_name', address.full_name)
        address.phone_no = data.get('phone_no', address.phone_no)
        address.address_line = data.get('address_line', address.address_line)
        address.city = data.get('city', address.city)
        address.thana = data.get('thana', address.thana)
        address.upozila = data.get('upozila', address.upozila)
        address.postal_code = data.get('postal_code', address.postal_code)
        address.note  = data.get('note',  address.note)
        address.save()

        return JsonResponse({
            'success': True,
            'address': {
                'full_name': address.full_name,
                'phone_no': address.phone_no,
                'address_line': address.address_line,
                'city': address.city,
                'thana': address.thana,
                'upozila': address.upozila,
                'postal_code': address.postal_code,
                'note': address.note or '',
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

@login_required
@require_POST
def update_shipping_method_ajax(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        shipping_method = data.get('shipping_method', '').strip()

        if not shipping_method:
            return JsonResponse({'success': False, 'error': 'shipping_method is required'}, status=400)

        order = get_object_or_404(admin_dashboard_models.Order, id=order_id)

        # Get the active delivery charge for this location
        try:
            charge = admin_dashboard_models.DeliveryCharge.objects.get(
                delivery_location=shipping_method,
                is_active=True
            )
        except admin_dashboard_models.DeliveryCharge.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'No active delivery charge for {shipping_method}'}, status=400)

        # Calculate total weight of order items
        import math
        total_weight_kg = sum(
            (item.product_attribute.weight_in_kg * item.quantity)
            for item in admin_dashboard_models.OrderItem.objects.filter(order=order).select_related('product_attribute')
            if item.product_attribute.weight
        )

        # Calculate shipping charge
        if charge.initial_weight >= total_weight_kg:
            new_shipping_charge = Decimal(str(charge.initial_charge))
        else:
            extra = math.ceil(total_weight_kg - charge.initial_weight)
            new_shipping_charge = Decimal(str(charge.initial_charge)) + Decimal(str(extra * charge.increment_weight_per_unit))

        # Update order
        order.shipping_method  = shipping_method
        order.shipping_charge  = new_shipping_charge

        # Recalculate grand total
        coupon_price = order.coupon_price or Decimal('0')
        vat = order.vat or Decimal('0')
        gst = order.gst or Decimal('0')
        sub_total = order.sub_total_after_discount or Decimal('0')

        order.total_payable = sub_total + new_shipping_charge - coupon_price + vat + gst
        order.save()

        return JsonResponse({
            'success': True,
            'shipping_method': shipping_method,
            'shipping_charge': float(new_shipping_charge),
            'new_total': float(order.total_payable),
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    


def order_detail_view(request, order_id):
    order = get_object_or_404(admin_dashboard_models.Order, id=order_id)
    product_item_obj = admin_dashboard_models.OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'product_item_obj': product_item_obj,
        "vat_gst": order.vat + order.gst

    }
    return render(request, 'custom-admin/orders/order_details.html', context)

@login_required
def search_ordered_product(request):
    search_words = request.GET.get('search_id')
    category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee__role='section_admin').values_list('category', flat=True)
    order_ids = admin_dashboard_models.OrderItem.objects.filter(product__categories__id__in=list(category_ids)).values_list('order', flat=True)
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = (
            admin_dashboard_models.Order.objects.filter(order_no__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(created_at__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(shipping_address__full_name__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(payment_status__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(order_status__icontains=search_words)
        )
    elif request.user.role == 'section_admin':
        obj_list = (
            admin_dashboard_models.Order.objects.filter(id__in=list(order_ids),order_no__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(id__in=list(order_ids),created_at__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(id__in=list(order_ids),shipping_address__full_name__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(id__in=list(order_ids),payment_status__icontains=search_words)|
            admin_dashboard_models.Order.objects.filter(id__in=list(order_ids),order_status__icontains=search_words)
        )
    context = {
        "orders": obj_list
    }
    return render(request, 'custom-admin/orders/search.html', context)


@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order = admin_dashboard_models.Order.objects.get(id=data['order_id'])
        order.order_status = data['order_status']

        if order.order_status == 'delivered': 
            order.delivery_date = timezone.now()
        order.save()
        return JsonResponse({"success": True, 'delivery_date': order.delivery_date})

@csrf_exempt
def update_payment_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order = admin_dashboard_models.Order.objects.get(id=data['order_id'])
        order.payment_status = data['payment_status']
        order.save()
        return JsonResponse({"success": True, 'payment_status': order.payment_status})
    

# ajax
@login_required
@require_POST
def update_order_ajax(request):
    try:
        data = json.loads(request.body)
        order_id  = data.get('order_id')
        order_status = data.get('order_status')
        payment_status = data.get('payment_status')
        items = data.get('items', [])

        order = get_object_or_404(admin_dashboard_models.Order, id=order_id)

        with transaction.atomic():
            if order_status:
                order.order_status = order_status
            if payment_status:
                order.payment_status = payment_status


            submitted_existing_ids = set()
            for item_data in items:

                if item_data.get('is_deleted'):
                    if not item_data.get('is_new'):
                        admin_dashboard_models.OrderItem.objects.filter(
                            id=item_data['id'], order=order
                        ).delete()
                    continue

                if item_data.get('is_new'):
                    attr_id = item_data.get('product_attribute_id')
                    if not attr_id:
                        continue
                    try:
                        attr = admin_dashboard_models.ProductAttribute.objects.get(id=attr_id)
                    except admin_dashboard_models.ProductAttribute.DoesNotExist:
                        continue

                    if not admin_dashboard_models.OrderItem.objects.filter(
                        order=order, product_attribute=attr
                    ).exists():
                        product_variant_obj = admin_dashboard_models.ProductVarient.objects.filter(
                            product=attr.product
                        ).first()
                        admin_dashboard_models.OrderItem.objects.create(
                            order=order,
                            product=attr.product,
                            product_attribute=attr,
                            product_variant=product_variant_obj,
                            price=attr.product_final_price,
                            quantity=item_data.get('quantity', 1),
                            buying_price=attr.buying_price,
                            tax_amount=Decimal('0.00'),
                        )

                # ── Update existing ──
                else:
                    item_id     = item_data.get('id')
                    quantity    = item_data.get('quantity', 1)
                    new_attr_id = item_data.get('new_product_attribute_id')

                    update_fields = {'quantity': quantity}

                    if new_attr_id:
                        try:
                            new_attr = admin_dashboard_models.ProductAttribute.objects.get(
                                id=new_attr_id
                            )
                            # Must use _id suffix — NOT passing instance to .update()
                            update_fields['product_attribute_id'] = new_attr.id
                            update_fields['price'] = new_attr.product_final_price
                            update_fields['buying_price'] = new_attr.buying_price

                            stock_status = new_attr.attribute_stock_status
                            if quantity > stock_status['remaining_stock']:
                                raise ValueError(
                                    f"Quantity {quantity} exceeds available stock "
                                    f"({stock_status['remaining_stock']}) for {new_attr.product.product_name}"
                                )
                            
                        except admin_dashboard_models.ProductAttribute.DoesNotExist:
                            pass  # keep original attribute, just update quantity
                    else:
                        try:
                            order_item = admin_dashboard_models.OrderItem.objects.get(id=item_id, order=order)
                            stock_status = order_item.product_attribute.attribute_stock_status
                            if quantity > stock_status['remaining_stock']:
                                raise ValueError(
                                    f"Quantity {quantity} exceeds available stock "
                                    f"({stock_status['remaining_stock']}) for "
                                    f"{order_item.product_attribute.product.product_name}"
                                )
                        except admin_dashboard_models.OrderItem.DoesNotExist:
                            pass

                    rows_updated = admin_dashboard_models.OrderItem.objects.filter(
                        id=item_id,
                        order=order   # ✅ Security: ensure item belongs to this order
                    ).update(**update_fields)

                    if rows_updated == 0:
                        # Item not found or doesn't belong to this order — skip silently
                        pass

                    submitted_existing_ids.add(item_id)

            # 3. Recalculate totals
            all_items = admin_dashboard_models.OrderItem.objects.filter(order=order).select_related(
                'product_attribute'
            )
            sub_total_after_discount = sum(
                item.product_attribute.product_final_price * item.quantity
                for item in all_items
            )
            shipping = order.shipping_charge or Decimal('0')
            coupon_price = order.coupon_price or Decimal('0')
            vat = order.vat or Decimal('0')
            gst = order.gst or Decimal('0')

            grand_total = (
                Decimal(str(sub_total_after_discount))
                + shipping
                - coupon_price
                + vat
                + gst
            )

            order.sub_total_after_discount = Decimal(str(sub_total_after_discount))
            order.total_payable = grand_total
            order.save()

        return JsonResponse({
            'success': True,
            'message': 'Order updated successfully.',
            'new_total': str(grand_total),
            'sub_total_after_discount': str(sub_total_after_discount),
        })

    except Exception as e:
        import traceback
        traceback.print_exc()  
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def search_products_ajax(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category_id', '')
    order_id = request.GET.get('order_id', '')

    # Get attribute IDs already in this order so we can exclude them
    already_added_attr_ids = set()
    if order_id:
        already_added_attr_ids = set(
            admin_dashboard_models.OrderItem.objects.filter(order_id=order_id)
            .values_list('product_attribute_id', flat=True)
        )
    

    attrs = admin_dashboard_models.ProductAttribute.objects.select_related(
        'product', 'color', 'size', 'product__sub_categories'
    ).exclude(id__in=already_added_attr_ids)
    

    if query:
        attrs = attrs.filter(product__product_name__icontains=query)
    if category_id:
        attrs = attrs.filter(product__categories_id=category_id)

    results = []
    for attr in attrs[:40]:   # limit to 40 results
        stock_status = attr.attribute_stock_status
        results.append({
            'product_attribute_id': attr.id,
            'product_id': attr.product.id,
            'name': attr.product.product_name,
            'size': str(attr.size) if attr.size else 'N/A',
            'color': str(attr.color) if attr.color else 'N/A',
            'price': float(attr.product_final_price),
            'stock': stock_status['remaining_stock'],
            'in_stock': stock_status['status'],
            'image': attr.image.url if attr.image else '',
            'category': attr.product.categories.name if attr.product.categories else '',
        })

    return JsonResponse({'products': results})