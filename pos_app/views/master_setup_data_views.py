import json
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from pos_app.models import pos_models
from pos_app.forms import master_setup_forms
from accounts_app.models import User

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
            form.save()
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
                instance = form.save(commit=False)
                instance.user_type = 'pos'
                instance.active_status = True
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