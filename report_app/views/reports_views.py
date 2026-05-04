from django.shortcuts import redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
from ..forms import report_forms
from admin_app.models import admin_dashboard_models
from collections import defaultdict


@login_required
def stock_reports_views(request):

    form = report_forms.StockReportForm()
    grouped_product_variants = {}
    grand_variant_total = 0
    grand_product_total = 0
    variants = None
    is_searched = False

    if request.method == "POST":
        category_id =  request.POST.get("categories")
        form = report_forms.StockReportForm(request.POST)
        if category_id:
            form.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id=category_id)
        
        if form.is_valid():            
            is_searched = True
            variants = admin_dashboard_models.ProductAttribute.objects.select_related(
                "product", "color", "size", "product_varient"
            )

            category = form.cleaned_data.get('categories')
            sub_category = form.cleaned_data.get('sub_categories')
            sub_sub_category = form.cleaned_data.get('sub_sub_categories')
            stock = form.cleaned_data.get('stock')

            if category:
                variants = variants.filter(product__categories=category)

            if sub_category:
                variants = variants.filter(product__sub_categories=sub_category)

            if sub_sub_category:
                variants = variants.filter(product__sub_sub_categories=sub_sub_category)

            variants = variants.order_by(
                'product__categories',
                'product__sub_categories',
                'product__sub_sub_categories',
                'product__product_name'
            )

            if stock is not None:
                variants = [
                    v for v in variants
                    if v.attribute_stock_status.get('remaining_stock', 0) <= stock
                ]

            variants_group = defaultdict(list)

            for v in variants:
                variants_group[v.product].append(v)

            grouped_product_variants = dict(variants_group)
            
            for product, variant_list in grouped_product_variants.items():
                total_stock = sum(
                    v.attribute_stock_status['remaining_stock']
                    for v in variant_list
                )
                

                grouped_product_variants[product] = {
                    'variants': variant_list,
                    'total_stock': total_stock
                }
                
                grand_product_total += total_stock
                grand_variant_total += sum(
                    v.attribute_stock_status.get('remaining_stock',0)
                    for v in variant_list
                )
                                
    context = {
        'form': form,
        'is_searched':is_searched,
        'grouped_products': grouped_product_variants,
        'grand_product_total': grand_product_total,
        'grand_variant_total': grand_variant_total
    }

    return render(request, 'custom-admin/reports/stock_reports.html', context)

    
@login_required
def order_report_views(request):
    order_obj = None
    is_searched = False
    total_buying_price, total_selling_price, total_profit, total_vat_gst, total_delivery_charge, ground_total, coupon_total = 0, 0, 0, 0, 0, 0, 0
    form = report_forms.OrderReportForm()
    if request.method == "POST":
        category_id =  request.POST.get("categories")
        form = report_forms.OrderReportForm(request.POST)
        category_id = request.POST.get('categories')
        if category_id:
            form.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id=category_id)
        if form.is_valid():
            is_searched = True
            category = form.cleaned_data.get('categories')
            sub_category = form.cleaned_data.get('sub_categories')
            sub_sub_category = form.cleaned_data.get('sub_sub_categories')
            order_status = form.cleaned_data.get('order_status')
            form_date = form.cleaned_data.get('form_date')
            to_date = form.cleaned_data.get('to_date')

            order_obj = admin_dashboard_models.Order.objects.all()

            if category:
                order_obj = order_obj.filter(order_items__product__categories=category)
            if sub_category:
                order_obj = order_obj.filter(order_items__product__sub_categories=sub_category)
            if sub_sub_category:
                order_obj = order_obj.filter(order_items__product__sub_sub_categories=sub_sub_category)
            if order_status:
                order_obj = order_obj.filter(order_status=order_status)
            if form_date and to_date:
                start = datetime.combine(form_date, time.min)
                end = datetime.combine(to_date, time.max)
                order_obj = order_obj.filter(created_at__gte=start, created_at__lte=end)

            order_obj = order_obj.distinct().order_by('-created_at')

            for order in order_obj:
                total_buying_price += order.order_wise_buying_price
                total_selling_price += order.order_wise_selling_price
                total_profit += order.order_wise_profit
                total_vat_gst += order.total_vat_gst_amount or 0
                total_delivery_charge += order.shipping_charge or 0
                ground_total += order.total_payable or 0
                coupon_total += order.coupon_price or 0


        else:
            print(form.errors)
    context = {
        'form': form,
        'is_searched': is_searched,
        'order_obj': order_obj,
        'total_buying_price': total_buying_price,
        'total_selling_price': total_selling_price,
        'total_profit': total_profit,
        'total_vat_gst': total_vat_gst,
        'total_delivery_charge': total_delivery_charge,
        'ground_total': ground_total,
        'coupon_total': coupon_total
    }
    return render(request, 'custom-admin/reports/order_report.html', context)