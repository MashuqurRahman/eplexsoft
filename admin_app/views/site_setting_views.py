from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from admin_app.models import admin_dashboard_models
from admin_app.forms import theme_setting_forms

@login_required
def site_setting_list(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            settings = admin_dashboard_models.SiteSetting.objects.all()
            return render(request, 'custom-admin/site_settings/index.html', {'settings': settings})
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def site_setting_create(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            if request.method == 'POST':
                form = theme_setting_forms.SiteSettingForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Information Added Successfully!!!")
                    return redirect('site_setting_list')
                else:
                    print(form.errors)
            else:
                form = theme_setting_forms.SiteSettingForm()
            context = {
                'form': form
            }
            return render(request, 'custom-admin/site_settings/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

@login_required
def site_setting_update(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            setting_obj = get_object_or_404(admin_dashboard_models.SiteSetting, pk=pk)
            if request.method == 'POST':
                form = theme_setting_forms.SiteSettingForm(request.POST, request.FILES, instance=setting_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Information Updated Successfully!!!")
                    return redirect('site_setting_list')
                else:
                    print(form.errors)
            else:
                form = theme_setting_forms.SiteSettingForm(instance=setting_obj)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/site_settings/update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def site_setting_delete(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            setting = get_object_or_404(admin_dashboard_models.SiteSetting, pk=pk)
            setting.delete()
            return redirect('site_setting_list')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
# PAYMENT METHODS VIEWS
@login_required
def payment_method_logs_list(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            payment_methods = admin_dashboard_models.paymentMethodLogos.objects.all()
            return render(request, 'custom-admin/payment_logos/index.html', {'logos': payment_methods})
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def payment_method_logo_create(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            if request.method == 'POST':
                form = theme_setting_forms.PaymentMethodLogoForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Payment Method Logo Added Successfully!!!")
                    return redirect('payment_method_logo_list')
                else:
                    print(form.errors)
            else:
                form = theme_setting_forms.PaymentMethodLogoForm()
            context = {
                'form': form
            }
            return render(request, 'custom-admin/payment_logos/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def payment_method_logo_delete(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            logo = get_object_or_404(admin_dashboard_models.paymentMethodLogos, pk=pk)
            logo.delete()
            return redirect('payment_method_logo_list')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

@login_required
def payment_method_logo_update(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            logo_obj = get_object_or_404(admin_dashboard_models.paymentMethodLogos, pk=pk)
            if request.method == 'POST':
                form = theme_setting_forms.PaymentMethodLogoForm(request.POST, request.FILES, instance=logo_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Payment Method Logo Updated Successfully!!!")
                    return redirect('payment_method_logo_list')
                else:
                    print(form.errors)
            else:
                form = theme_setting_forms.PaymentMethodLogoForm(instance=logo_obj)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/payment_logos/update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')