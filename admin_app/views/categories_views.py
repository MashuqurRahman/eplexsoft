from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Page, PageNotAnInteger, Paginator, EmptyPage
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from ..models import admin_dashboard_models
from ..forms import categories_forms

def format_form_errors(form):
    errors = []
    for field, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{field.replace('_', ' ').title()}: {error}")
    return errors

@login_required
def categories_index_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = admin_dashboard_models.Categories.objects.all().order_by('-id')

    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        obj_list = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids)).order_by('-id')
    else:
        return render(request, 'permission_denied.html')
    
    page = request.GET.get('page')
    paginator = Paginator(obj_list, 30)
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)

    context = {
        'obj_list': obj_list
    }
    return render(request, 'custom-admin/categories/index.html', context)


@login_required
def add_categories_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin':
        form = categories_forms.CategoriesForm()
        if request.method == "POST":
            form = categories_forms.CategoriesForm(request.POST,request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Categories Added Successfully!!!")
                    return redirect('categories_list_url')
                except Exception as e:
                    messages.error(request, f"Error: {str(e)}")
            else:
                if form.errors:
                    for error in format_form_errors(form):
                        messages.error(request, error)
        context = {
            'form': form
        }
        return render(request, 'custom-admin/categories/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def update_categories_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin':
        get_obj = admin_dashboard_models.Categories.objects.get(id=pk)
        form = categories_forms.CategoriesForm(instance=get_obj)
        if request.method == "POST":
            form = categories_forms.CategoriesForm(request.POST,request.FILES, instance=get_obj)
            if form.is_valid():
                form.save()
                messages.success(request, "Categories Updated Successfully!!!")
                return redirect('categories_list_url')
            else:
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'custom-admin/categories/edit.html', context)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_categories_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin':
        try:
            get_obj = get_object_or_404(admin_dashboard_models.Categories, id=pk)
            get_obj.delete()
            messages.success(request, "Categories Deleted Successfully!!!")
            return redirect('categories_list_url')
        except ProtectedError:
            messages.error(request, "This category cannot be deleted because it is linked to existing sub-categories or products.")
            return redirect('categories_list_url')
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def search_categories_view(request):
    search_words = request.GET.get('search_id')
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = (
            admin_dashboard_models.Categories.objects.filter(name__icontains=search_words)|
            admin_dashboard_models.Categories.objects.filter(description__icontains=search_words)
        )
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee__role='section_admin').values_list('category', flat=True)
        obj_list = (
            admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids), name__icontains=search_words)|
            admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids), description__icontains=search_words)
        )
    else:
        return render(request, 'permission_denied.html')
    context = {
        "obj_list": obj_list
    }
    return render(request, 'custom-admin/categories/search.html', context)
    

@login_required
def sub_categories_index_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = admin_dashboard_models.SubCategories.objects.all().order_by('-id')
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        obj_list = admin_dashboard_models.SubCategories.objects.filter(categories__id__in=list(category_ids)).order_by('-id')
    else:
        return render(request, 'permission_denied.html')
    
    page = request.GET.get('page')
    paginator = Paginator(obj_list, 30)
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)

    context = {
        'obj_list': obj_list
    }
    return render(request, 'custom-admin/sub_categories/index.html', context)

@login_required
def add_sub_categories_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        form = categories_forms.SubCategoriesForm(user=request.user, role=request.user.role)
        if request.method == "POST":
            form = categories_forms.SubCategoriesForm(request.POST, request.FILES, user=request.user, role=request.user.role)
            if form.is_valid():
                form.save()
                messages.success(request, "Sub Categories Added Successfully!!!")
                return redirect('sub_categories_index_url')
            else:
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'custom-admin/sub_categories/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def update_sub_categories_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        get_obj = admin_dashboard_models.SubCategories.objects.get(id=pk)
        form = categories_forms.SubCategoriesForm(instance=get_obj, user=request.user, role=request.user.role)
        if request.method == "POST":
            form = categories_forms.SubCategoriesForm(request.POST, request.FILES, instance=get_obj, user=request.user, role=request.user.role)
            if form.is_valid():
                form.save()
                messages.success(request, "Sub Categories Updated Successfully!!!")
                return redirect('sub_categories_index_url')
            else:
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'custom-admin/sub_categories/edit.html', context)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_sub_categories_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        try:
            get_obj = get_object_or_404(admin_dashboard_models.SubCategories, id=pk)
            get_obj.delete()
            messages.success(request, "Categories Deleted Successfully!!!")
            return redirect('sub_categories_index_url')
        except ProtectedError:
            messages.error(request, "This sub category cannot be deleted because it is linked to existing sub-sub-categories or products.")
            return redirect('sub_categories_index_url')
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def search_sub_categories_view(request):
    search_words = request.GET.get('search_id')

    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = (
            admin_dashboard_models.SubCategories.objects.filter(categories__name__icontains=search_words)|
            admin_dashboard_models.SubCategories.objects.filter(sub_cat_name__icontains=search_words)|
            admin_dashboard_models.SubCategories.objects.filter(description__icontains=search_words)
        )
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee__role='section_admin').values_list('category', flat=True)
        obj_list = (
            admin_dashboard_models.SubCategories.objects.filter(categories__id__in=list(category_ids), categories__name__icontains=search_words)|
            admin_dashboard_models.SubCategories.objects.filter(categories__id__in=list(category_ids), sub_cat_name__icontains=search_words)|
            admin_dashboard_models.SubCategories.objects.filter(categories__id__in=list(category_ids), description__icontains=search_words)
        )
    else:
        return render(request, 'permission_denied.html')

    context = {
        "obj_list": obj_list
    }
    return render(request, 'custom-admin/sub_categories/search.html', context)
    
# SUB SUB CATEGORIES
@login_required
def sub_sub_categories_index_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = admin_dashboard_models.SubSubCategories.objects.all().order_by('-id')
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        obj_list = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories__id__in=list(category_ids)).order_by('-id')
    else:
        return render(request, 'permission_denied.html')

    page = request.GET.get('page')
    paginator = Paginator(obj_list, 30)
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)

    context = {
        'obj_list': obj_list
    }
    return render(request, 'custom-admin/sub_sub_categories/index.html', context)

@login_required
def add_sub_sub_categories_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        form = categories_forms.SubSubCategoriesForm(user=request.user, role=request.user.role)
        if request.method == "POST":
            form = categories_forms.SubSubCategoriesForm(request.POST, request.FILES, user=request.user, role=request.user.role)
            if form.is_valid():
                form.save()
                messages.success(request, "Sub Sub Categories Added Successfully!!!")
                return redirect('sub_sub_cat_index_url')
            else:
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'custom-admin/sub_sub_categories/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def update_sub_sub_categories_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        get_obj = admin_dashboard_models.SubSubCategories.objects.get(id=pk)
        form = categories_forms.SubSubCategoriesForm(instance=get_obj, user=request.user, role=request.user.role)
        form.fields['categories'].initial = get_obj.sub_categories.categories
        form.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.filter(categories__id=get_obj.sub_categories.categories.id)
        if request.method == "POST":
            form = categories_forms.SubSubCategoriesForm(request.POST, request.FILES, instance=get_obj, user=request.user, role=request.user.role)
            if form.is_valid():
                form.save()
                messages.success(request, "Sub Sub Categories Updated Successfully!!!")
                return redirect('sub_sub_cat_index_url')
            else:
                messages.error(request, "Invalid form")
        context = {
            'form': form
        }
        return render(request, 'custom-admin/sub_sub_categories/edit.html', context)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_sub_sub_categories_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        try:
            get_obj = get_object_or_404(admin_dashboard_models.SubSubCategories, id=pk)
            get_obj.delete()
            messages.success(request, "Sub Sub Categories Deleted Successfully!!!")
            return redirect('sub_sub_cat_index_url')
        except:
            messages.error(request, "This sub sub category cannot be deleted because it is linked to existing products.")
            return redirect('sub_sub_cat_index_url')
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def search_sub_sub_categories_view(request):
    search_words = request.GET.get('search_id')
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = (
            admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories__name__icontains=search_words)|
            admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__sub_cat_name__icontains=search_words)|
            admin_dashboard_models.SubSubCategories.objects.filter(sub_sub_cat_name__icontains=search_words)
        )
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee__role='section_admin').values_list('category', flat=True)
        obj_list = (
            admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories__id__in=list(category_ids),sub_categories__categories__name__icontains=search_words)|
            admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories__id__in=list(category_ids),sub_categories__sub_cat_name__icontains=search_words)|
            admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories__id__in=list(category_ids),sub_sub_cat_name__icontains=search_words)
        )
    else:
        return render(request, 'permission_denied.html')
    context = {
        "obj_list": obj_list
    }
    return render(request, 'custom-admin/sub_sub_categories/search.html', context)