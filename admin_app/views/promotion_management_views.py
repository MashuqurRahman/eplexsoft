from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Page, PageNotAnInteger, Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from ..models import admin_dashboard_models
from ..forms import promotion_management_forms
from django.db import IntegrityError


@login_required
def product_flash_sell_index_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = admin_dashboard_models.FlashSell.objects.all().order_by('-id')
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        obj_list = admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids)).order_by('-id')
    else:
        return render(request, 'permission_denied.html')
    
    page = request.GET.get('page')
    paginator = Paginator(obj_list, 50)
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)

    context = {
        'obj_list': obj_list
    }
    return render(request, 'custom-admin/flash_sell/index.html', context)


@login_required
def product_flash_sell_create_view(request):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=request.user, employee__role=request.user.role).values_list('category', flat=True)
        form = promotion_management_forms.FlashSellForm()
        if request.user.role == 'section_admin' or request.user.role == 'employee':
            form.fields['category'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))
        if request.method == "POST":
            form = promotion_management_forms.FlashSellForm(request.POST)
            if request.user.role == 'section_admin' or request.user.role == 'employee':
                form.fields['category'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))
            selected_products = request.POST.getlist('select_product')
            
        
            if not selected_products:
                messages.error(request, "Please select at least one product.")
                return redirect(request.path)
            
            if form.is_valid():
                side_slider = form.cleaned_data["side_slider"]

                try:
                    with transaction.atomic():
                        discount_amount = form.cleaned_data["discount_amount"]

                        for pid in selected_products:
                            attributes = admin_dashboard_models.ProductAttribute.objects.filter(product_id=pid)




                            for attr in attributes:
                                if discount_amount >= attr.regular_price or (
                                    attr.discount_price and discount_amount >= attr.discount_price
                                ):
                                    messages.error(
                                        request,
                                        "Discount amount must be less than Regular Price or Discount Price"
                                    )
                                    return redirect(request.path)
                                
                            
                        try:   

                            objs = [
                                admin_dashboard_models.FlashSell(
                                    product_id=pid,
                                    discount_amount=discount_amount,
                                    is_percentage=form.cleaned_data["is_percentage"],
                                    side_slider=form.cleaned_data["side_slider"],
                                )
                                for pid in selected_products
                            ]

                            admin_dashboard_models.FlashSell.objects.bulk_create(objs)
                            for pid in selected_products:
                                attributes = admin_dashboard_models.ProductAttribute.objects.filter(product_id=pid)
                                for attr in attributes:
                                    pk_obj = admin_dashboard_models.ProductAttribute.objects.filter(pk=attr.pk)
                                    pk_obj.update(
                                        final_price=attr.calculate_final_price()
                                    )

                        except Exception as e:
                            messages.error(request, "{}".format(e))
                            return redirect(request.path)
                    

                        messages.success(request, "Product is Sucessfully Added to Flash Sell!!!")
                        return redirect('flash_sell_index_url')
                except Exception as e:
                    messages.error(request, f"Error: {str(e)}")
            else:
                print(form.errors)
        context = {
            'form': form
        }
        return render(request, 'custom-admin/flash_sell/create.html', context)
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def product_flash_sell_update_view(request, pk):
    get_obj = admin_dashboard_models.FlashSell.objects.get(id=pk)
    form = promotion_management_forms.FlashSellUpdateForm(instance=get_obj)
    form.fields['category'].initial = get_obj.product.categories
    form.fields['sub_category'].initial = get_obj.product.sub_categories
    form.fields['sub_sub_category'].initial = get_obj.product.sub_sub_categories
    if request.method == "POST":
        form = promotion_management_forms.FlashSellUpdateForm(request.POST, instance=get_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Product is Updated Sucessfully!!!")
            return redirect('flash_sell_index_url')
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'custom-admin/flash_sell/update.html', context)

@login_required
def product_flash_sell_delete_view(request, pk):
    if request.user.is_superuser or request.user.role == 'central_admin' or request.user.role == 'section_admin' or request.user.role == 'employee':
        try:
            get_obj = get_object_or_404(admin_dashboard_models.FlashSell, id=pk)
            get_obj.delete()
            messages.success(request, "Product is Deleted Sucessfully!!!")
            return redirect('flash_sell_index_url')
        except:
            messages.error(request, "Delete is not possible")
            return redirect('flash_sell_index_url')
    else:
        return render(request, 'permission_denied.html')
    
@login_required
def flash_sale_search_view(request):
    search_words = request.GET.get('search_id')    
    if request.user.is_superuser or request.user.role == 'central_admin':
        obj_list = (
            admin_dashboard_models.FlashSell.objects.filter(side_slider__campaign_name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(side_slider__campaign_type__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__categories__name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__sub_categories__sub_cat_name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__sub_sub_categories__sub_sub_cat_name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__product_name__icontains=search_words)
        )
    elif request.user.role == 'section_admin' or request.user.role == 'employee':
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee__role='section_admin').values_list('category', flat=True)
        obj_list = (
            admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids),side_slider__campaign_name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids),side_slider__campaign_type__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids),product__categories__name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids),product__sub_categories__sub_cat_name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids),product__sub_sub_categories__sub_sub_cat_name__icontains=search_words)|
            admin_dashboard_models.FlashSell.objects.filter(product__categories__id__in=list(category_ids),product__product_name__icontains=search_words)
        )
    else:
        return render(request, 'permission_denied.html')
    
    context = {
        "obj_list": obj_list
    }
    return render(request, 'custom-admin/flash_sell/search.html', context)