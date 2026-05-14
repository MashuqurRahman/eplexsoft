from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Page, Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from ..forms import slider_forms
from ..models import admin_dashboard_models
from client_app.models import client_models
from accounts_app.models import User

@login_required
def all_employee_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = User.objects.all()[1:]
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        obj_list = User.objects.filter(employee_of_category__category_id__in=list(category_ids), role='employee').order_by('-id')
    else:
        return render(request, 'permission_denied.html')
    
    page = request.GET.get('page')
    paginator = Paginator(obj_list, 10)
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)

    context = {
        'obj_list': obj_list
    }
    return render(request, 'custom-admin/employee/index.html', context)

@login_required
def add_employee_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin':
        form = slider_forms.EmployeeForm(user=request.user, role=request.user.role)
        if request.method == "POST":
            form = slider_forms.EmployeeForm(request.POST, user=request.user, role=request.user.role)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        employee = form.save(commit=False)
                        employee.save()

                        categories = form.cleaned_data.get('category')

                        for category in categories:
                            admin_dashboard_models.EmployeeCategories.objects.create(
                                employee = employee,
                                category = category
                            )
                        messages.success(request, "Employee Added Successfully!!!")
                        return redirect('all_employee_url')
                    
                except Exception as e:
                    print("Error: ", str(e))
                    messages.error(request, f"Error: {str(e)}")
            else:
                print("+++++++",form.errors)
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'custom-admin/employee/create.html', context)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def update_employee_details_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin':
        get_obj = get_object_or_404(User, id=pk)

        if request.method == "POST":
            form = slider_forms.EmployeeUpdateForm(request.POST, instance=get_obj, user=request.user, role=request.user.role)

            if form.is_valid():
                if get_obj.role and get_obj.role.lower() == 'customer':
                    messages.error(request, "Customer information cannot be updated!")
                else:
                    user = form.save()
                    admin_dashboard_models.EmployeeCategories.objects.filter(
                        employee=user
                    ).delete()

                    for cat in form.cleaned_data['category']:
                        admin_dashboard_models.EmployeeCategories.objects.create(
                            employee=user,
                            category=cat
                        )

                    messages.success(request, "Employee Information Updated Successfully!")
                    return redirect('all_employee_url')
            else:
                messages.error(request, "Invalid form")

        else:
            existing_categories = admin_dashboard_models.EmployeeCategories.objects.filter(employee=get_obj).values_list('category_id', flat=True)
            form = slider_forms.EmployeeUpdateForm(instance=get_obj, initial={'category': existing_categories}, user=request.user, role=request.user.role)

        return render(request, 'custom-admin/employee/update.html', {'form': form})
    else:
        return render(request, 'permission_denied.html')


@login_required
def empolyee_profile_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin':
        employee_obj = User.objects.get(id=pk)
        return render(request, 'custom-admin/employee/profile.html', {'employee': employee_obj})
    else:
        return render(request, 'permission_denied.html')
@login_required
def delete_employee_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin':
        try:
            get_obj = get_object_or_404(User, id=pk)
            get_obj.delete()
            messages.success(request, "Employee Deleted Successfully!!!")
            return redirect('all_employee_url')
        except:
            messages.error(request, "Delete is not possible")
            return redirect('all_employee_url')
    else:
        return render(request, 'permission_denied.html')

@login_required   
def search_empolyee_view(request):
    search_words = request.GET.get('search_id')
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = (
            User.objects.filter(name__icontains=search_words)|
            User.objects.filter(email__icontains=search_words)|
            User.objects.filter(gender__icontains=search_words)|
            User.objects.filter(role__icontains=search_words)|
            User.objects.filter(phone__icontains=search_words)
        )
    elif request.user.role == 'section_admin':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        obj_list = User.objects.filter(employee_of_category__category_id__in=list(category_ids), role='employee').order_by('-id')
        obj_list = (
            User.objects.filter(employee_of_category__category_id__in=list(category_ids), role='employee',name__icontains=search_words)|
            User.objects.filter(employee_of_category__category_id__in=list(category_ids), role='employee',email__icontains=search_words)|
            User.objects.filter(employee_of_category__category_id__in=list(category_ids), role='employee',gender__icontains=search_words)|
            User.objects.filter(employee_of_category__category_id__in=list(category_ids), role='employee',role__icontains=search_words)|
            User.objects.filter(employee_of_category__category_id__in=list(category_ids), role='employee',phone__icontains=search_words)
        )
    else:
        return render(request, 'permission_denied.html')
    context = {
        "obj_list": obj_list
    }
    return render(request, 'custom-admin/employee/search.html', context)