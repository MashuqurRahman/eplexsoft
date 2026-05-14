from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Page, PageNotAnInteger, Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import admin_dashboard_models
from ..forms import delivery_management_forms

def format_form_errors(form):
    errors = []
    for field, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{field.replace('_', ' ').title()}: {error}")
    return errors

@login_required
def coupon_management_index_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("coupon_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            obj_list = admin_dashboard_models.CouponManagement.objects.all().order_by('-id')
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
            return render(request, 'custom-admin/coupon_management/index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def coupon_management_create_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("coupon_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            form = delivery_management_forms.CouponManagementForm()
            if request.method == "POST":
                form = delivery_management_forms.CouponManagementForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "New Coupon Created Successfully!!!")
                    return redirect('coupon_index_url')
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/coupon_management/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def coupon_management_update_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("coupon_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            get_obj = admin_dashboard_models.CouponManagement.objects.get(id=pk)
            form = delivery_management_forms.CouponManagementUpdateForm(instance=get_obj)
            if request.method == "POST":
                form = delivery_management_forms.CouponManagementUpdateForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Coupon Updated Successfully!!!")
                    return redirect('coupon_index_url')
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/coupon_management/update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def coupon_management_delete_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("coupon_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            try:
                get_obj = get_object_or_404(admin_dashboard_models.CouponManagement, id=pk)
                get_obj.delete()
                messages.success(request, "Coupon Deleted Successfully!!!")
                return redirect('coupon_index_url')
            except Exception as e:
                messages.error(request, f"Delete is not possible, {str(e)}")
                return redirect('coupon_index_url')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def search_coupon_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("coupon_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):   
            search_words = request.GET.get('search_id')
            obj_list = (
                admin_dashboard_models.CouponManagement.objects.filter(name__icontains=search_words)|
                admin_dashboard_models.CouponManagement.objects.filter(code__icontains=search_words)|
                admin_dashboard_models.CouponManagement.objects.filter(value__icontains=search_words)|
                admin_dashboard_models.CouponManagement.objects.filter(type__icontains=search_words)|
                admin_dashboard_models.CouponManagement.objects.filter(min_price__icontains=search_words)|
                admin_dashboard_models.CouponManagement.objects.filter(number_of_user__icontains=search_words)
            )
            context = {
                "obj_list": obj_list
            }
            return render(request, 'custom-admin/coupon_management/search.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')