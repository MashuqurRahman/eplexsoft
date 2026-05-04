from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Page, PageNotAnInteger, Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import admin_dashboard_models
from ..forms import delivery_management_forms

@login_required
def delivery_charge_index_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            obj_list = admin_dashboard_models.DeliveryCharge.objects.all().order_by('-id')
            page = request.GET.get('page')
            paginator = Paginator(obj_list, 20)
            try:
                obj_list = paginator.page(page)
            except PageNotAnInteger:
                obj_list = paginator.page(1)
            except EmptyPage:
                obj_list = paginator.page(paginator.num_pages)

            context = {
                'obj_list': obj_list
            }
            return render(request, 'custom-admin/delivery_charge/index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

@login_required
def delivery_charge_create_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            form = delivery_management_forms.DeliveryChargeForm()
            if request.method == "POST":
                form = delivery_management_forms.DeliveryChargeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Delivery Charge Added Successfully!!!")
                    return redirect('delivery_charge_index_url')
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/delivery_charge/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delivery_charge_update_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            get_obj = admin_dashboard_models.DeliveryCharge.objects.get(id=pk)
            form = delivery_management_forms.DeliveryChargeForm(instance=get_obj)
            if request.method == "POST":
                form = delivery_management_forms.DeliveryChargeForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Delivery Charge Updated Successfully!!!")
                    return redirect('delivery_charge_index_url')
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/delivery_charge/update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delivery_charge_delete_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            try:
                get_obj = get_object_or_404(admin_dashboard_models.DeliveryCharge, id=pk)
                get_obj.delete()
                messages.success(request, "Delivery Charge Deleted Successfully!!!")
                return redirect('delivery_charge_index_url')
            except:
                messages.error(request, "Delete is not possible")
                return redirect('delivery_charge_index_url')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

# DELIVERY DISCOUNT

@login_required
def delivery_discount_index_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            obj_list = admin_dashboard_models.DeliveryDiscount.objects.all().order_by('-id')
            page = request.GET.get('page')
            paginator = Paginator(obj_list, 20)
            try:
                obj_list = paginator.page(page)
            except PageNotAnInteger:
                obj_list = paginator.page(1)
            except EmptyPage:
                obj_list = paginator.page(paginator.num_pages)

            context = {
                'obj_list': obj_list
            }
            return render(request, 'custom-admin/delivery_discount/index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delivery_discount_create_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            form = delivery_management_forms.DeliveryDiscountForm()
            if request.method == "POST":
                form = delivery_management_forms.DeliveryDiscountForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Delivery Discount Added Successfully!!!")
                    return redirect('delivery_discount_index_url')
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/delivery_discount/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delivery_discount_update_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            get_obj = admin_dashboard_models.DeliveryDiscount.objects.get(id=pk)
            form = delivery_management_forms.DeliveryDiscountForm(instance=get_obj)
            if request.method == "POST":
                form = delivery_management_forms.DeliveryDiscountForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Delivery Discount Updated Successfully!!!")
                    return redirect('delivery_discount_index_url')
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/delivery_discount/update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delivery_discount_delete_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("delivery_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            try:
                get_obj = get_object_or_404(admin_dashboard_models.DeliveryDiscount, id=pk)
                get_obj.delete()
                messages.success(request, "Delivery Discount Deleted Successfully!!!")
                return redirect('delivery_discount_index_url')
            except:
                messages.error(request, "Delete is not possible")
                return redirect('delivery_discount_index_url')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')