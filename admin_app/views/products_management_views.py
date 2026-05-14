from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Page, PageNotAnInteger, EmptyPage, Paginator
from django.contrib import messages
from ..models import admin_dashboard_models
from ..forms import product_management_forms

@login_required
def brand_list_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            obj_list = admin_dashboard_models.Brand.objects.all().order_by('-id')

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
            return render(request, 'custom-admin/brand/index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def add_brand_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = product_management_forms.BrandForm()
            if request.method == "POST":
                form = product_management_forms.BrandForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Brand Added Successfully!!!")
                    return redirect('brand_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/brand/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def update_brand_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            get_obj = admin_dashboard_models.Brand.objects.get(id=pk)
            form = product_management_forms.BrandForm(instance=get_obj)
            if request.method == "POST":
                form = product_management_forms.BrandForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Brand Updated Successfully!!!")
                    return redirect('brand_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/brand/edit.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_brand_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            try:
                get_obj = get_object_or_404(admin_dashboard_models.Brand, id=pk)
                get_obj.delete()
                messages.success(request, "Brand Deleted Successfully!!!")
                return redirect('brand_list_url')
            except:
                messages.error(request, "Delete is not possible")
                return redirect('brand_list_url')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def search_brand_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
        search_words = request.GET.get('search_id')
        obj_list = (
            admin_dashboard_models.Brand.objects.filter(name__icontains=search_words)
        )
        context = {
            "obj_list": obj_list
        }
        return render(request, 'custom-admin/brand/search.html', context)
    else:
       return render(request, 'permission_denied.html')
     
# Color views

@login_required
def color_list_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            obj_list = admin_dashboard_models.Color.objects.all().order_by('-id')

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
            return render(request, 'custom-admin/color/index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def add_color_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = product_management_forms.ColorForm()
            if request.method == "POST":
                form = product_management_forms.ColorForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Color Added Successfully!!!")
                    return redirect('color_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/color/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def update_color_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            get_obj = admin_dashboard_models.Color.objects.get(id=pk)
            form = product_management_forms.ColorForm(instance=get_obj)
            if request.method == "POST":
                form = product_management_forms.ColorForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Color Updated Successfully!!!")
                    return redirect('color_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/color/edit.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_color_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            try:
                get_obj = get_object_or_404(admin_dashboard_models.Color, id=pk)
                get_obj.delete()
                messages.success(request, "Color Deleted Successfully!!!")
                return redirect('color_list_url')
            except:
                messages.error(request, "Delete is not possible")
                return redirect('color_list_url')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def search_color_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            search_words = request.GET.get('search_id')
            obj_list = (
                admin_dashboard_models.Color.objects.filter(name__icontains=search_words)|
                admin_dashboard_models.Color.objects.filter(hex_code__icontains=search_words)
            )
            context = {
                "obj_list": obj_list
            }
            return render(request, 'custom-admin/color/search.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
# Size views

@login_required
def size_list_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
    
            obj_list = admin_dashboard_models.Size.objects.all().order_by('-id')

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
            return render(request, 'custom-admin/size/index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def add_size_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = product_management_forms.SizeForm()
            if request.method == "POST":
                form = product_management_forms.SizeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Size Added Successfully!!!")
                    return redirect('size_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/size/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def update_size_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            get_obj = admin_dashboard_models.Size.objects.get(id=pk)
            form = product_management_forms.SizeForm(instance=get_obj)
            if request.method == "POST":
                form = product_management_forms.SizeForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Size Updated Successfully!!!")
                    return redirect('size_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/size/edit.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_size_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            try:
                get_obj = get_object_or_404(admin_dashboard_models.Size, id=pk)
                get_obj.delete()
                messages.success(request, "Size Deleted Successfully!!!")
                return redirect('size_list_url')
            except:
                messages.error(request, "Delete is not possible")
                return redirect('size_list_url')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def search_size_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            search_words = request.GET.get('search_id')
            obj_list = (
                admin_dashboard_models.Size.objects.filter(value__icontains=search_words)
            )
            context = {
                "obj_list": obj_list
            }
            return render(request, 'custom-admin/size/search.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
# Unit views

@login_required
def unit_list_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            obj_list = admin_dashboard_models.Unit.objects.all().order_by('-id')

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
            return render(request, 'custom-admin/unit/index.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

@login_required
def add_unit_view(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            form = product_management_forms.UnitForm()
            if request.method == "POST":
                form = product_management_forms.UnitForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Unit Added Successfully!!!")
                    return redirect('unit_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/unit/create.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')
    
@login_required
def update_unit_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            get_obj = admin_dashboard_models.Unit.objects.get(id=pk)
            form = product_management_forms.UnitForm(instance=get_obj)
            if request.method == "POST":
                form = product_management_forms.UnitForm(request.POST, instance=get_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Unit Updated Successfully!!!")
                    return redirect('unit_list_url')
                else:
                    messages.error(request, "Invalid form")
            context = {
                'form': form
            }
            return render(request, 'custom-admin/unit/edit.html', context)
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')

@login_required
def delete_unit_view(request, pk):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("product_variant_management" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            try:
                get_obj = get_object_or_404(admin_dashboard_models.Unit, id=pk)
                get_obj.delete()
                messages.success(request, "Unit Deleted Successfully!!!")
                return redirect('unit_list_url')
            except:
                messages.error(request, "Delete is not possible")
                return redirect('unit_list_url')
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')