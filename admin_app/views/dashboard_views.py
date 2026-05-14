from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_app.models import admin_dashboard_models
from client_app.models import client_models
from accounts_app.models import User

@login_required
def admin_dashboard_view(request):
    all_orders = total_pending_order = total_confirmed_order = total_shipped_order = total_delivered_order = total_cancelled_order = total_returned_order = 0
    total_category,total_sub_category,total_product,total_contact,total_flash_sell = [],[],[],[],[]
    total_contact = client_models.Contact.objects.count()
    if request.user.is_superuser or request.user.role == 'central_admin':
        total_category = admin_dashboard_models.Categories.objects.count()
        total_sub_category = admin_dashboard_models.SubCategories.objects.count()
        total_product = admin_dashboard_models.Product.objects.count()
        total_flash_sell = admin_dashboard_models.FlashSell.objects.count()

        all_orders = admin_dashboard_models.Order.objects.all().count()
        total_pending_order = admin_dashboard_models.Order.objects.filter(order_status='pending').count()
        total_confirmed_order = admin_dashboard_models.Order.objects.filter(order_status='confirmed').count()
        total_shipped_order = admin_dashboard_models.Order.objects.filter(order_status='shipped').count()
        total_delivered_order = admin_dashboard_models.Order.objects.filter(order_status='delivered').count()
        total_cancelled_order = admin_dashboard_models.Order.objects.filter(order_status='cancelled').count()
        total_returned_order = admin_dashboard_models.Order.objects.filter(order_status='returned').count()

    if request.user.role == 'section_admin':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role='section_admin').values_list('category', flat=True)
        total_category = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids)).count()
        total_sub_category = admin_dashboard_models.SubCategories.objects.filter(categories__id__in=list(category_ids)).count()
        total_product = admin_dashboard_models.Product.objects.filter(categories__id__in=list(category_ids)).count()
        total_flash_sell = admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids)).count()

        all_orders = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids)).count()
        total_pending_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='pending').count()
        total_confirmed_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='confirmed').count()
        total_shipped_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='shipped').count()
        total_delivered_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='delivered').count()
        total_cancelled_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='cancelled').count()
        total_returned_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='returned').count()

    if request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role='employee').values_list('category', flat=True)
        total_category = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids)).count()
        total_sub_category = admin_dashboard_models.SubCategories.objects.filter(categories__id__in=list(category_ids)).count()
        total_product = admin_dashboard_models.Product.objects.filter(categories__id__in=list(category_ids)).count()
        total_flash_sell = admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids)).count()

        all_orders = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids)).count()
        total_pending_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='pending').count()
        total_confirmed_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='confirmed').count()
        total_shipped_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='shipped').count()
        total_delivered_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='delivered').count()
        total_cancelled_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='cancelled').count()
        total_returned_order = admin_dashboard_models.Order.objects.filter(order_items__product__categories__id__in=list(category_ids), order_status='returned').count()

    context = {
        'total_category': total_category,
        'total_sub_category': total_sub_category,
        'total_product': total_product,
        'total_contact': total_contact,
        'total_flash_sell': total_flash_sell,

        'all_orders': all_orders,
        'total_pending_order': total_pending_order,
        'total_confirmed_order': total_confirmed_order,
        'total_shipped_order': total_shipped_order,
        'total_delivered_order': total_delivered_order,
        'total_cancelled_order': total_cancelled_order,
        'total_returned_order': total_returned_order,
    }
    return render(request, 'custom-admin/index.html', context)