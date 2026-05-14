from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Page, Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from client_app.models import client_models
from admin_app.models import admin_dashboard_models
from client_app.forms import client_forms

@login_required
def admin_contact_view(request):
    obj_list = client_models.Contact.objects.all().order_by('-id')
    context = {
        'obj_list': obj_list
    }
    return render(request, 'custom-admin/conversations/contact.html', context)

# TERMS AND CONDITIONS
@login_required
def terms_and_condition_index_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            obj_list = admin_dashboard_models.TermsCondition.objects.all().order_by('-id')
            context = {
                'obj_list': obj_list
            }
            return render(request, 'custom-admin/footer/terms_condition_index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def terms_and_conditions_create_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = client_forms.TearmsConditionForm()
            if request.method == "POST":
                form = client_forms.TearmsConditionForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Terms and Condition added successfully!!!")
                    return redirect("terms_and_conditions_index_url")
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/footer/terms_condition_create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def terms_and_conditions_update_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            get_obj = admin_dashboard_models.TermsCondition.objects.get(id=pk)
            form = client_forms.TearmsConditionForm(instance=get_obj)
            if request.method == "POST":
                form = client_forms.TearmsConditionForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Terms and Condition updated successfully!!!")
                    return redirect("terms_and_conditions_index_url")
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/footer/terms_condition_update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def terms_and_conditions_delete_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            try:
                admin_dashboard_models.TermsCondition.objects.get(id=pk).delete()
                messages.success(request, "Terms & Condition Deleted Successfully!!!")
                return redirect("terms_and_conditions_index_url")
            except:
                messages.error(request, "Delete is not possible")
                return redirect("terms_and_conditions_index_url")
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

# PRIVECY AND POLICY

@login_required
def privecy_and_policy_index_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            obj_list = admin_dashboard_models.PrivacyPolicy.objects.all()
            context = {
                'obj_list': obj_list
            }
            return render(request, 'custom-admin/footer/privecy_policy_index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def privecy_and_policy_create_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = client_forms.PrivecyPolicyForm()
            if request.method == "POST":
                form = client_forms.PrivecyPolicyForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Privecy policy added successfully!!!")
                    return redirect("privecy_and_policy_index_url")
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/footer/privecy_policy_create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def privecy_and_policy_update_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            get_obj = admin_dashboard_models.PrivacyPolicy.objects.get(id=pk)
            form = client_forms.PrivecyPolicyForm(instance=get_obj)
            if request.method == "POST":
                form = client_forms.PrivecyPolicyForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Privecy policy updated successfully!!!")
                    return redirect("privecy_and_policy_index_url")
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/footer/privecy_policy_update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def privecy_and_policy_delete_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            try:
                admin_dashboard_models.PrivacyPolicy.objects.get(id=pk).delete()
                messages.success(request, "Privecy Policy Deleted Successfully!!!")
                return redirect("privecy_and_policy_index_url")
            except:
                messages.error(request, "Delete is not possible")
                return redirect("privecy_and_policy_index_url")
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
# ABOUT US

@login_required
def about_us_index_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            obj_list = admin_dashboard_models.AboutUs.objects.all()
            context = {
                'obj_list': obj_list
            }
            return render(request, 'custom-admin/footer/about_us_index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

@login_required
def about_us_create_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = client_forms.AboutUsForm()
            if request.method == "POST":
                form = client_forms.AboutUsForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "About us content added successfully!!!")
                    return redirect("about_us_index_url")
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/footer/about_us_create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    

@login_required
def about_us_update_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            get_obj = admin_dashboard_models.AboutUs.objects.get(id=pk)
            form = client_forms.AboutUsForm(instance=get_obj)
            if request.method == "POST":
                form = client_forms.AboutUsForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "About us content updated successfully!!!")
                    return redirect("about_us_index_url")
                else:
                    print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'custom-admin/footer/about_us_update.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def about_us_delete_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("company_info_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            try:
                admin_dashboard_models.AboutUs.objects.get(id=pk).delete()
                messages.success(request, "About us Deleted Successfully!!!")
                return redirect("about_us_index_url")
            except:
                messages.error(request, "Delete is not possible")
                return redirect("about_us_index_url")
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')