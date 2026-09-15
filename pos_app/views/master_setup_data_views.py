import json
import hashlib
from django.contrib import messages
from django.db import transaction, models
from django.db.models import Q, Count
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from pos_app.models import pos_models
from pos_app.forms import master_setup_forms
from accounts_app.models import User
from admin_app.models import admin_dashboard_models

@login_required
def branch_setup_view(request):

    edit_branch = None
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_branch = get_object_or_404(pos_models.BrachName, pk=edit_id)

    if request.method == "POST" and "save_branch" in request.POST:
        branch_id = request.POST.get("branch_id") 
        instance = get_object_or_404(pos_models.BrachName, pk=branch_id) if branch_id else None

        form = master_setup_forms.BranchForm(request.POST, instance=instance)
        if form.is_valid():
            branch = form.save(commit=False)
            if not branch_id:
                branch.active_status = True
            branch.save()
            messages.success(request, "Branch updated." if branch_id else "Branch added.")
            return redirect("branch_setup_url")
        else:
            edit_branch = instance
    else:
        form = master_setup_forms.BranchForm(instance=edit_branch)

    branches = pos_models.BrachName.objects.all()
    active_brance_count = branches.filter(active_status=True).count()
    inactive_brance_count = branches.filter(active_status=False).count()
    pos_user_count = User.objects.filter(user_type='pos').count()


    context = {
        "form": form,
        "branches": branches,
        "branch_count": branches.count(),
        "staff_assigned_count": 0,
        "edit_branch": edit_branch,
        "pos_user_count": pos_user_count,
        "active_brance_count": active_brance_count,
        "inactive_brance_count": inactive_brance_count,
    }
    
    return render(request, 'pos/master_setup/branch/create.html', context)

@login_required
@require_POST
def branch_delete_view(request, pk):
    branch = get_object_or_404(pos_models.BrachName, id=pk)
    branch.delete()
    return redirect('branch_setup_url')

# USER SETUP

@login_required
def pos_user_list_view(request):
    obj_list = User.objects.filter(user_type='pos').order_by('-id')
    context = {
        'obj_list': obj_list
    }
    return render(request, 'pos/master_setup/user/index.html', context)


@login_required
def pos_user_create_view(request):
    if request.user.is_superuser:
        form = master_setup_forms.UserSetupForm()
        if request.method == "POST":
            form = master_setup_forms.UserSetupForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('password')
                instance = form.save(commit=False)
                instance.user_type = 'pos'
                instance.active_status = True
                instance.set_password(password)
                instance.save()

                messages.success(request, "User Added Successfully!!!")
                return redirect('pos_user_list_url')
                    
            else:
                print(form.errors)
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'pos/master_setup/user/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def pos_user_update_view(request, pk):
    if request.user.is_superuser:
        get_obj = User.objects.get(id=pk)
        form = master_setup_forms.UserSetupUpdateForm(instance=get_obj)
        if request.method == "POST":
            form = master_setup_forms.UserSetupUpdateForm(request.POST, instance=get_obj)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user_type = 'pos'
                instance.save()

                messages.success(request, "User Updated Successfully!!!")
                return redirect('pos_user_list_url')
                    
            else:
                print(form.errors)
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'pos/master_setup/user/update.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def pos_user_delete_view(request, pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    messages.success(request, f'User "{user.name}" removed.')
    return redirect('pos_user_list_url')

@login_required
def pos_user_search_view(request):
    search_text = request.GET.get('search_text').strip()
    user_obj = User.objects.filter(user_type='pos').order_by('-id')
    obj_list = user_obj.filter(
        Q(name__icontains=search_text)|
        Q(email__icontains=search_text)|
        Q(phone__icontains=search_text)|
        Q(gender__icontains=search_text)|
        Q(pos_branch__name__icontains=search_text)
    )
    return render(request, 'pos/master_setup/user/search.html', {'obj_list': obj_list})


# CUSTOMER SETUP

@login_required
def pos_customer_index_view(request):
    obj_list = pos_models.Customer.objects.all().order_by('-id')
    context = {
        'obj_list': obj_list
    }
    return render(request, 'pos/master_setup/customer/index.html', context)

@login_required
def pos_customer_create_view(request):
    if request.user.is_superuser:
        form = master_setup_forms.CustomerSetupForm()
        if request.method == "POST":
            form = master_setup_forms.CustomerSetupForm(request.POST)
            if form.is_valid():
                form.save()

                messages.success(request, "Customer Added Successfully!!!")
                return redirect('pos_customer_index_url')
                    
            else:
                print(form.errors)
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'pos/master_setup/customer/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def pos_customer_update_view(request, pk):
    if request.user.is_superuser:
        get_obj = pos_models.Customer.objects.get(id=pk)
        form = master_setup_forms.CustomerSetupForm(instance=get_obj)
        if request.method == "POST":
            form = master_setup_forms.CustomerSetupForm(request.POST, instance=get_obj)
            if form.is_valid():
                form.save()

                messages.success(request, "Customer Updated Successfully!!!")
                return redirect('pos_customer_index_url')
                    
            else:
                print(form.errors)
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'pos/master_setup/customer/update.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def pos_customer_delete_view(request, pk):
    customer = get_object_or_404(pos_models.Customer, id=pk)
    customer.delete()
    messages.success(request, f'Customer "{customer.name}" removed.')
    return redirect('pos_customer_index_url')

@login_required
def pos_customer_search_view(request):
    search_text = request.GET.get('search_text').strip()
    customer_obj = pos_models.Customer.objects.all().order_by('-id')
    obj_list = customer_obj.filter(
        Q(name__icontains=search_text)|
        Q(email__icontains=search_text)|
        Q(phone__icontains=search_text)|
        Q(address__icontains=search_text)|
        Q(branch__name__icontains=search_text)
    )
    return render(request, 'pos/master_setup/customer/search.html', {'obj_list': obj_list})

# POS PRODUCT

@login_required
def pos_product_list_view(request):
    if request.user.is_superuser:
        obj_list = pos_models.PosProduct.objects.select_related(
            'attribute__product__categories',
            'attribute__product__sub_categories',
            'attribute__product_varient',
            'branch',
        ).all().order_by("-id")
    else:
        obj_list = pos_models.PosProduct.objects.select_related(
            'attribute__product__categories',
            'attribute__product__sub_categories',
            'attribute__product_varient',
            'branch',
        ).filter(branch_id=request.user.pos_branch.id).order_by("-id")

    context = {
        'obj_list': obj_list,
        'categories': admin_dashboard_models.Categories.objects.all(),
        'total_categories': admin_dashboard_models.Categories.objects.count(),
        'total_subcategories': admin_dashboard_models.SubCategories.objects.count(),
    }
    return render(request, 'pos/master_setup/product/index.html', context)


@login_required
def pos_product_create_view(request):
    if request.user.is_superuser:
        form = master_setup_forms.PosProductFrom()
        if request.method == "POST":
            form = master_setup_forms.PosProductFrom(request.POST)
            if form.is_valid():
                form.save()

                messages.success(request, "Product Added Successfully!!!")
                return redirect('pos_product_list_url')
                    
            else:
                print(form.errors)
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'pos/master_setup/product/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def pos_product_update_view(request, pk):
    if request.user.is_superuser:
        get_obj = get_object_or_404(pos_models.PosProduct, id=pk)
        form = master_setup_forms.PosProductFrom(instance=get_obj)
        if request.method == "POST":
            form = master_setup_forms.PosProductFrom(request.POST, instance=get_obj)
            if form.is_valid():
                form.save()

                messages.success(request, "Product Updated Successfully!!!")
                return redirect('pos_product_list_url')
                    
            else:
                print(form.errors)
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'pos/master_setup/product/update.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def pos_product_delete_view(request, pk):
    product = get_object_or_404(pos_models.PosProduct, id=pk)
    product.delete()
    messages.success(request, "Product Deleted Successfully!!!")
    return redirect('pos_product_list_url')

@login_required
def pos_product_search_view(request):
    search_text = request.GET.get('search_text', '').strip()
    category_id = request.GET.get('category', 'All')
    sub_category_id = request.GET.get('sub_category', 'All')

    obj_list = pos_models.PosProduct.objects.select_related(
        'attribute__product__categories',
        'attribute__product__sub_categories',
        'attribute__product_varient',
        'branch',
    ).all().order_by('-id')

    if category_id and category_id != 'All':
        obj_list = obj_list.filter(attribute__product__categories_id=category_id)

    if sub_category_id and sub_category_id != 'All':
        obj_list = obj_list.filter(attribute__product__sub_categories_id=sub_category_id)

    if search_text:
        obj_list = obj_list.filter(
            Q(attribute__product__product_name__icontains=search_text) |
            Q(attribute__product__categories__name__icontains=search_text) |
            Q(attribute__product__sub_categories__sub_cat_name__icontains=search_text) |
            Q(branch__name__icontains=search_text) |
            Q(attribute__product_varient__sku__icontains=search_text)
        )

    html = render_to_string(
        'pos/master_setup/product/product_table_partial.html',{'obj_list': obj_list}, request=request
    )
    return JsonResponse({'html': html, 'count': obj_list.count()})

@login_required
def pos_get_subcategories_view(request):
    category_id = request.GET.get('category_id')
    if not category_id or category_id == 'All':
        subs = admin_dashboard_models.SubCategories.objects.none()
    else:
        subs = admin_dashboard_models.SubCategories.objects.filter(categories_id=category_id)

    data = [{'id': s.id, 'name': s.sub_cat_name} for s in subs]
    return JsonResponse({'sub_categories': data})


# STOCK TRANSFER 

@login_required
def pos_pull_request_list(request):
    branch_id = request.GET.get('branch_id')
    if request.user.is_superuser:
        qs = pos_models.StockPullRequest.objects.select_related('attribute', 'requesting_branch', 'source_branch').all()
    else:
        qs = pos_models.StockPullRequest.objects.select_related('attribute', 'requesting_branch', 'source_branch').filter(requesting_branch_id=request.user.pos_branch.id)

    if branch_id:
        qs = qs.filter(requesting_branch_id=branch_id)
    attributes = admin_dashboard_models.ProductAttribute.objects.all()
    branches = pos_models.BrachName.objects.all()

    summary = qs.aggregate(
        total_sent = Count('id'),
        total_pending = Count('id', filter=Q(status='pending')),
        total_approved = Count('id', filter=Q(status='approved')),
    )
    context = {
        'qs': qs,
        'attributes': attributes,
        'branches': branches,
        'total_sent': summary['total_sent'],
        'pending_count': summary['total_pending'],
        'approved_count': summary['total_approved'],
    }
    return render(request, 'pos/master_setup/stock_transfer/sent_requests.html', context)


@login_required
def pos_create_pull_request(request):
    if request.method != 'POST':
        return redirect('pull_request_list_url')

    attribute_id = request.POST.get('attribute_id')
    requesting_branch_id  = request.user.pos_branch.id
    source_branch_id   = request.POST.get('source_branch_id')
    qty = int(request.POST.get('requested_qty', 0) or 0)

    if requesting_branch_id == source_branch_id:
        messages.error(request, 'Requesting branch and source branch must be different.')
        return redirect('pull_request_list_url')

    if qty <= 0:
        messages.error(request, 'Requested quantity must be greater than zero.')
        return redirect('pull_request_list_url')

    pull_request = pos_models.StockPullRequest.objects.create(
        attribute_id=attribute_id,
        requesting_branch_id=requesting_branch_id,
        source_branch_id=source_branch_id,
        requested_qty=qty,
        request_by=request.user,
    )

    pos_models.StockTransferLog.objects.create(
        pull_request=pull_request,
        event='requested',
        attribute_id=attribute_id,
        requesting_branch_id=requesting_branch_id,
        source_branch_id=source_branch_id,
        qty=qty,
        acted_by=request.user,
    )

    messages.success(request, 'Pull request sent.')
    return redirect('pull_request_list_url')


@login_required
def pos_received_pull_requests(request):
    branch_id = request.GET.get('branch_id')
    if request.user.is_superuser:
        qs = pos_models.StockPullRequest.objects.select_related('attribute', 'requesting_branch', 'source_branch').filter(status='pending')
    else:
        qs = pos_models.StockPullRequest.objects.select_related('attribute', 'requesting_branch', 'source_branch').filter(status='pending', source_branch_id=request.user.pos_branch.id)

    if branch_id:
        qs = qs.filter(source_branch_id=branch_id)
    return render(request, 'pos/master_setup/stock_transfer/received_requests.html', {'requests': qs})

@login_required
@transaction.atomic
def pos_approve_pull_request(request, pk):
    pull_request = get_object_or_404(pos_models.StockPullRequest.objects.select_for_update(), pk=pk, status='pending')

    source_stock, _ = pos_models.PosProduct.objects.select_for_update().get_or_create(
        attribute_id=pull_request.attribute_id,
        branch_id=pull_request.source_branch_id,
        defaults={'stock': 0},
    )

    if source_stock.stock < pull_request.requested_qty:
        messages.error(request,f'Insufficient stock at {pull_request.source_branch}. Available: {source_stock.stock}.')
        return redirect('received_pull_requests_url')
    
    dest_stock, _ = pos_models.PosProduct.objects.select_for_update().get_or_create(
        attribute_id=pull_request.attribute_id,
        branch_id=pull_request.requesting_branch_id,
        defaults={'stock': 0},
    )

    source_stock.stock -= pull_request.requested_qty
    dest_stock.stock += pull_request.requested_qty
    source_stock.save(update_fields=['stock'])
    dest_stock.save(update_fields=['stock'])

    pull_request.status = 'approved'
    pull_request.reviewed_by = request.user
    pull_request.reviewed_at = timezone.now()
    pull_request.save(update_fields=['status', 'reviewed_by', 'reviewed_at'])

    pos_models.StockTransferLog.objects.create(
        pull_request=pull_request,
        event='approved',
        attribute_id=pull_request.attribute_id,
        requesting_branch_id=pull_request.requesting_branch_id,
        source_branch_id=pull_request.source_branch_id,
        qty=pull_request.requested_qty,
        source_stock_after=source_stock.stock,
        dest_stock_after=dest_stock.stock,
        acted_by=request.user,
    )

    messages.success(request, 'Pull request approved. Stock transferred.')
    return redirect('received_pull_requests_url')

login_required
def pos_reject_pull_request(request, pk):
    pull_request = get_object_or_404(pos_models.StockPullRequest, pk=pk, status='pending')
    pull_request.status = 'rejected'
    pull_request.reviewed_by = request.user
    pull_request.reviewed_at = timezone.now()
    pull_request.reject_reason = request.POST.get('reject_reason', '')
    pull_request.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'reject_reason'])

    pos_models.StockTransferLog.objects.create(
        pull_request=pull_request,
        event='rejected',
        attribute_id=pull_request.attribute_id,
        requesting_branch_id=pull_request.requesting_branch_id,
        source_branch_id=pull_request.source_branch_id,
        qty=pull_request.requested_qty,
        acted_by=request.user,
    )
    messages.success(request, 'Pull request rejected.')
    return redirect('received_pull_requests_url')

@login_required
def pos_stock_transfer_history(request):
    branches = pos_models.BrachName.objects.all()
    qs = pos_models.StockTransferLog.objects.select_related('attribute', 'requesting_branch', 'source_branch', 'acted_by')

    form = master_setup_forms.TransferHistoryFilterForm()
    if request.method == "POST":
        form = master_setup_forms.TransferHistoryFilterForm(request.POST)
        if form.is_valid():
            branch_id = form.cleaned_data.get('branch_id')
            event = form.cleaned_data.get('event')

            if branch_id:
                qs = qs.filter(models.Q(requesting_branch_id=branch_id) | models.Q(source_branch_id=branch_id))
            if event:
                qs = qs.filter(event=event)

    context = {
        'branches': branches,
        'logs': qs,
        'form': form
    }
    return render(request, 'pos/master_setup/stock_transfer/transfer_history.html', context)