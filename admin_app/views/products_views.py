from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Page, Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.db import transaction
from django.contrib import messages
from ..models import admin_dashboard_models
from ..forms import products_forms

def format_form_errors(form):
    errors = []
    for field, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{field.replace('_', ' ').title()}: {error}")
    return errors

@login_required
def product_list_index_view(request):

    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = admin_dashboard_models.Product.all_objects.all().order_by('-id')
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        obj_list = admin_dashboard_models.Product.objects.filter(categories__id__in=list(category_ids)).order_by('-id')
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
    return render(request, 'custom-admin/products/index.html', context)

@login_required
def add_product_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        form = products_forms.ProductForm(user=request.user, role=request.user.role)
        varient_form = products_forms.ProductVarientForm()
        ProdctAttributeFormset = modelformset_factory(
            admin_dashboard_models.ProductAttribute,
            form = products_forms.ProductAttributeForm,
            extra=1,
            can_delete=True
        )
        form.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.none()
        form.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.none()
        product_attribute_formset = ProdctAttributeFormset(queryset=admin_dashboard_models.ProductAttribute.objects.none(), prefix='product_formset')
        if request.method == "POST":
            form = products_forms.ProductForm(request.POST, request.FILES, user=request.user, role=request.user.role)
            varient_form = products_forms.ProductVarientForm(request.POST, request.FILES)
            product_attribute_formset = ProdctAttributeFormset(request.POST, request.FILES, prefix='product_formset')
            if form.is_valid() and varient_form.is_valid() and product_attribute_formset.is_valid():
                try:
                    with transaction.atomic():
                        has_cover = False 
                        for attribute_form in product_attribute_formset:
                            if not attribute_form.cleaned_data:
                                continue

                            regular_price = attribute_form.cleaned_data.get('regular_price')
                            discount_price = attribute_form.cleaned_data.get('discount_price')
                            is_cover = attribute_form.cleaned_data.get('is_cover')

                            if is_cover:
                                has_cover = True

                            if discount_price is not None and discount_price >= regular_price:
                                messages.error(
                                    request,
                                    "Discount price must be less than regular price."
                                )
                                raise ValueError("Invalid discount price")
                            
                        if not has_cover:
                            messages.error(request, "Please select at least one cover photo in is cover section")
                            raise ValueError("Cover image not selected")
                            

                        product = form.save()
                        product.cover_product_attribute =None
                        varient_form_instance = varient_form.save(commit=False)
                        varient_form_instance.product = product
                        varient_form_instance.save()
                        
                        attribute_instances  = product_attribute_formset.save(commit=False)
                        for index, instance in enumerate(attribute_instances):
                            instance.product = product
                            instance.product_varient = varient_form_instance
                            instance.save()

                            image_filed_name = f'attribute_images_{index}'
                            image_files = request.FILES.getlist(image_filed_name)
                            if image_files:
                                for image in image_files:
                                    admin_dashboard_models.ProductAttributeImage.objects.create(
                                        product_attribute=instance,
                                        image=image
                                    )
                            
                        messages.success(request, "Product Added Successfully!!!")
                        return redirect('products_list_url')
                except Exception as e:
                    messages.error(request, f"Error: {e}")
            else:
                if form.errors:
                    for error in format_form_errors(form):
                        messages.error(request, error)
                elif varient_form.errors:
                    for error in format_form_errors(varient_form):
                        messages.error(request, error)
                else:
                    for form_errors in product_attribute_formset.errors:
                        for field, errors in form_errors.items():
                            for error in errors:
                                messages.error(request, f"{field.replace('_',' ').title()}: {error}")

        context = {
            'form': form,
            'varient_form': varient_form,
            'product_attribute_formset': product_attribute_formset
        }
        return render(request, 'custom-admin/products/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def update_product_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        get_obj = admin_dashboard_models.Product.all_objects.get(id=pk)
        varient_obj = admin_dashboard_models.ProductVarient.objects.get(product=get_obj.id)
        attribute_obj = admin_dashboard_models.ProductAttribute.objects.filter(product=get_obj).first()
        form = products_forms.ProductForm(instance=get_obj, user=request.user, role=request.user.role)
        varient_form = products_forms.ProductVarientForm(instance=varient_obj)
        total_sold_qty = get_obj.total_sold_count['sold_qty']                   #nja
        form.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.filter(categories=get_obj.categories.id)
        form.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories=get_obj.sub_categories.id)
        if request.method == "POST":
            form = products_forms.ProductForm(request.POST, request.FILES, instance=get_obj, user=request.user, role=request.user.role)
            varient_form = products_forms.ProductVarientForm(request.POST, request.FILES, instance=varient_obj)
            if form.is_valid() and varient_form.is_valid():
                try:
                    with transaction.atomic():
                        product = form.save(commit=False)
                        varient_form_instance = varient_form.save(commit=False)
                        varient_form_instance.product = product
                        varient_form_instance.save()
                        product.cover_product_attribute = attribute_obj
                        product.save()
                        
                        messages.success(request, "Product Updated Successfully!!!")
                        return redirect('products_list_url')
                except Exception as e:
                    messages.error(request, f"Error: str{e}")
            else:
                messages.error(request, "Invalid form")
        context = {
            'form': form,
            'varient_form': varient_form,
            'total_sold_qty':total_sold_qty
        }
        return render(request, 'custom-admin/products/edit.html', context)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_product_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        try:
            get_obj = get_object_or_404(admin_dashboard_models.Product, id=pk)
            get_obj.delete()
            messages.success(request, "Product Deleted Successfully!!!")
            return redirect('products_list_url')
        except Exception as e:
            print(f"Error: str{e}")
            messages.error(request, "Delete is not possible")
            return redirect('products_list_url')
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def product_details_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        product_obj = admin_dashboard_models.Product.all_objects.prefetch_related('product_attribute', 'product_varient').get(id=pk)
        product_varient_obj = admin_dashboard_models.ProductVarient.objects.get(product=product_obj.id)
        product_attribures_obj = admin_dashboard_models.ProductAttribute.objects.filter(product=product_obj.id).order_by('-id')
        context = {
            'product': product_obj,
            'product_varient': product_varient_obj,
            'product_attribures_obj': product_attribures_obj,
        }
        return render(request, 'custom-admin/products/details.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def search_products_view(request):
    search_words = request.GET.get('search_id')

    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = (
            admin_dashboard_models.Product.objects.filter(categories__name__icontains=search_words)|
            admin_dashboard_models.Product.objects.filter(sub_categories__sub_cat_name__icontains=search_words)|
            admin_dashboard_models.Product.objects.filter(sub_sub_categories__sub_sub_cat_name__icontains=search_words)|
            admin_dashboard_models.Product.objects.filter(product_name__icontains=search_words)
        )
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee__role='section_admin').values_list('category', flat=True)
        obj_list = (
            admin_dashboard_models.Product.objects.filter(categories__id__in=list(category_ids),categories__name__icontains=search_words)|
            admin_dashboard_models.Product.objects.filter(categories__id__in=list(category_ids),sub_categories__sub_cat_name__icontains=search_words)|
            admin_dashboard_models.Product.objects.filter(categories__id__in=list(category_ids),sub_sub_categories__sub_sub_cat_name__icontains=search_words)|
            admin_dashboard_models.Product.objects.filter(categories__id__in=list(category_ids),product_name__icontains=search_words)
        )
    else:
        return render(request, 'permission_denied.html')
    
    context = {
        "obj_list": obj_list
    }
    return render(request, 'custom-admin/products/search.html', context)

# PRODUCT ATTRIBUTES

@login_required
def product_attribute_create_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        product_obj = admin_dashboard_models.Product.objects.get(id=pk)
        varient_obj = admin_dashboard_models.ProductVarient.objects.get(product__id=pk)
        form = products_forms.AddProductAttributeForm()
        if request.method == "POST":
            form = products_forms.AddProductAttributeForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        attribute_images = request.FILES.getlist('attribute_images')
                        instance = form.save(commit=False)
                        instance.product = product_obj
                        instance.product_varient = varient_obj
                        instance.save()
                        
                        if attribute_images:
                            for image in attribute_images:
                                admin_dashboard_models.ProductAttributeImage.objects.create(product_attribute=instance, image=image)

                        messages.success(request, "Product Varient Attribute Added Successfully!!!")
                        return redirect('product_details_url', product_obj.id)
                except Exception as e:
                    messages.error(request, f"Error: {e}")
            else:
                print(form.errors)
        context = {
            'form': form
        }
        return render(request, 'custom-admin/product_attribute/create.html', context)
    else:
        return render(request, 'permission_denied.html')

@login_required
def product_attribute_update_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        get_obj = admin_dashboard_models.ProductAttribute.objects.get(id=pk)
        existing_images = get_obj.product_attribute_image.all()
        form = products_forms.UpdateProductAttributeForm(instance=get_obj)
        stock = get_obj.attribute_stock_status.get('remaining_stock')
        if request.method == "POST":
            form = products_forms.UpdateProductAttributeForm(request.POST, request.FILES, instance=get_obj)
            if form.is_valid():
                attribute_images = request.FILES.getlist('attribute_images')
                form = form.save(commit=False)
                quantity = request.POST.get('quantity')
                total_qty = get_obj.stock + int(quantity)
                if total_qty < 0:
                    messages.error(request, "Quantity cannot be less than sold quantity")
                    return redirect('product_attribute_update_url', get_obj.product.id)
                form.stock = total_qty
                form.save()

                if attribute_images:
                    for image in attribute_images:
                        admin_dashboard_models.ProductAttributeImage.objects.create(product_attribute=form, image=image)

                messages.success(request, "Product Varient Attribute Updated Successfully!!!")
                return redirect('product_details_url', get_obj.product.id)
            else:
                messages.error(request, "Please correct the errors below.")
        context = {
            'form': form,
            'stock': stock,
            'existing_images': existing_images
        }
        return render(request, 'custom-admin/product_attribute/update.html', context)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def product_attribute_delete_view(request, pk, product_id):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        get_obj = None
        try:
            product_obj = admin_dashboard_models.Product.objects.prefetch_related('product_attribute').get(id=product_id)
            product_attribures_obj = admin_dashboard_models.ProductAttribute.objects.filter(product=product_obj.id).order_by('-id')
            get_obj = get_object_or_404(admin_dashboard_models.ProductAttribute, id=pk)
            if len(product_attribures_obj) > 1:
                get_obj.delete()
                messages.success(request, "Product Varient Attribute Deleted Successfully!!!")
                return redirect('product_details_url', get_obj.product.id)
            else:
                messages.error(request, "Please keep at least one attribute of this product")
                return redirect('product_details_url', get_obj.product.id)
        except Exception as e:
            messages.error(request, "Delete is not possible")
            return redirect('product_details_url', get_obj.product.id)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def delete_attribute_image(request, pk):
    image = admin_dashboard_models.ProductAttributeImage.objects.get(id=pk)
    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('product_attribute_update_url', image.product_attribute.id)
from django.http import JsonResponse
from django.urls import reverse
def product_suggestion(request):
    q = request.GET.get("q", "")

    data = []

    if q:
        products =admin_dashboard_models.Product.objects.filter(product_name__icontains=q)[:8]

        data = [
            {
                "id": p.id,
                "name": p.product_name,
                "url": reverse("product_details_page_url", args=[p.id])
            }
            for p in products
        ]

    return JsonResponse(data, safe=False)