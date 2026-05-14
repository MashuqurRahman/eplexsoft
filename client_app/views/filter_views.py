from django.http import JsonResponse
from admin_app.models import admin_dashboard_models

def get_subcategories(request):
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')
    if categories:
        sub_categories = admin_dashboard_models.SubCategories.objects.filter(categories_id__in=categories).values('id','sub_cat_name')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        sub_categories = admin_dashboard_models.SubCategories.objects.filter(categories_id__in=category_ids).values('id','sub_cat_name')
    else:
        sub_categories = admin_dashboard_models.SubCategories.objects.all().values('id','sub_cat_name') 

    return JsonResponse(list(sub_categories), safe=False)


    # if categories and brands:
    #     sub_categories = admin_dashboard_models.SubCategories.objects.filter(
    #         categories_id__in=categories,
    #         product_sub_categories__product_varient__brand_id__in=brands
    #     ).values('id', 'sub_cat_name').distinct()
    # elif categories:
    #     sub_categories = admin_dashboard_models.SubCategories.objects.filter(
    #         categories_id__in=categories
    #     ).values('id', 'sub_cat_name').distinct()
    # else:
    #     sub_categories = admin_dashboard_models.SubCategories.objects.all().values('id', 'sub_cat_name')

    # return JsonResponse(list(sub_categories), safe=False)

def get_subsubcategories(request):
    sub_categories = request.GET.getlist('sub_categories[]')
    categories = request.GET.getlist('categories[]')
    sub_category_id = request.GET.get('sub_category_id')
    brands = request.GET.getlist('brands[]')
    if sub_categories:
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories_id__in=sub_categories).values('id','sub_sub_cat_name')
    elif categories:
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id__in=categories).values('id','sub_sub_cat_name')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id__in=category_ids).values('id','sub_sub_cat_name')
    else:
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.all().values('id','sub_sub_cat_name')

    return JsonResponse(list(sub_sub_categories), safe=False)

def get_subsub_categories_from_category(request):
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')
    if categories:
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id__in=categories).values('id','sub_sub_cat_name')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id__in=category_ids).values('id','sub_sub_cat_name')
    else:
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.all().values('id','sub_sub_cat_name')

    return JsonResponse(list(sub_sub_categories), safe=False)

def get_brands_from_category(request):
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')
    if categories:
        brand_ids = admin_dashboard_models.ProductVarient.objects.filter(product__categories_id__in=categories).values_list('brand_id', flat=True).distinct()
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brand_ids).values('id','name')
    elif brands:
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brands).values('id','name')
    else:
        brands = admin_dashboard_models.Brand.objects.all().values('id','name')

    return JsonResponse(list(brands), safe=False)

def get_colors_from_category(request):
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')
    if categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    else:
        colors = admin_dashboard_models.Color.objects.all().values('id','name')

    return JsonResponse(list(colors), safe=False)

def get_sizes_from_category(request):
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')
    if categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    else:
        sizes = admin_dashboard_models.Size.objects.all().values('id','value')

    return JsonResponse(list(sizes), safe=False)


# SUB CATEGORY

def get_brands_from_sub_category(request):
    sub_categories = request.GET.getlist('sub_categories[]')
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')
    if sub_categories:
        brand_ids = admin_dashboard_models.ProductVarient.objects.filter(product__sub_categories_id__in=sub_categories).values_list('brand_id', flat=True).distinct()
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brand_ids).values('id','name')
    elif categories:
        brand_ids = admin_dashboard_models.ProductVarient.objects.filter(product__categories_id__in=categories).values_list('brand_id', flat=True).distinct()
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brand_ids).values('id','name')
    elif brands:
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brands).values('id','name')
    else:
        brands = admin_dashboard_models.Brand.objects.all().values('id','name')

    return JsonResponse(list(brands), safe=False)

def get_colors_from_sub_category(request):
    sub_categories = request.GET.getlist('sub_categories[]')
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')
    if sub_categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    else:
        colors = admin_dashboard_models.Color.objects.all().values('id','name')

    return JsonResponse(list(colors), safe=False)

def get_sizes_from_sub_category(request):
    sub_categories = request.GET.getlist('sub_categories[]')
    categories = request.GET.getlist('categories[]')
    brands = request.GET.getlist('brands[]')

    if sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    else:
        sizes = admin_dashboard_models.Size.objects.all().values('id','value')

    return JsonResponse(list(sizes), safe=False)


# SUB SUB CATEGORY
def get_brands_from_sub_sub_category(request):
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    brands = request.GET.getlist('brands[]')

    if sub_sub_categories:
        brand_ids = admin_dashboard_models.ProductVarient.objects.filter(product__sub_sub_categories_id__in=sub_sub_categories).values_list('brand_id', flat=True).distinct()
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brand_ids).values('id','name')
    elif sub_categories:
        brand_ids = admin_dashboard_models.ProductVarient.objects.filter(product__sub_categories_id__in=sub_categories).values_list('brand_id', flat=True).distinct()
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brand_ids).values('id','name')
    elif categories:
        brand_ids = admin_dashboard_models.ProductVarient.objects.filter(product__categories_id__in=categories).values_list('brand_id', flat=True).distinct()
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brand_ids).values('id','name')
    elif brands:
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brands).values('id','name')
    else:
        brands = admin_dashboard_models.Brand.objects.all().values('id','name')

    return JsonResponse(list(brands), safe=False)

def get_colors_from_sub_sub_category(request):
    sub_sub_categories = [x for x in request.GET.getlist('sub_sub_categories[]') if x]
    sub_categories = [x for x in request.GET.getlist('sub_categories[]') if x]
    categories = [x for x in request.GET.getlist('categories[]') if x]
    brands = [x for x in request.GET.getlist('brands[]') if x]

    # sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    # categories = request.GET.getlist('categories[]')
    # sub_categories = request.GET.getlist('sub_categories[]')

    if sub_sub_categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_sub_categories_id__in=sub_sub_categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    
    elif sub_categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    else:
        colors = admin_dashboard_models.Color.objects.all().values('id','name')

    return JsonResponse(list(colors), safe=False)

def get_sizes_from_sub_sub_category(request):
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    brands = request.GET.getlist('brands[]')
    if sub_sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_sub_categories_id__in=sub_sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brands:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands).values_list('product__categories_id', flat=True).distinct()
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    else:
        sizes = admin_dashboard_models.Size.objects.all().values('id','value')

    return JsonResponse(list(sizes), safe=False)

def get_sizes_from_brand(request):
    brand_ids = request.GET.getlist('brand_ids[]')
    brands_ids = request.GET.getlist('brands_ids[]')
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    if brand_ids and sub_sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__sub_sub_categories_id__in=sub_sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brand_ids and sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__sub_categories_id__in=sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brand_ids and categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__categories_id__in=categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brand_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_sub_categories_id__in=sub_sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brands_ids:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands_ids).values_list('product__categories_id', flat=True).distinct()
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    else:
        sizes = admin_dashboard_models.Size.objects.all().values('id','value')

    return JsonResponse(list(sizes), safe=False)

def get_colors_from_brand(request):
    brand_ids = request.GET.getlist('brand_ids[]')
    brands_ids = request.GET.getlist('brands_ids[]')
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    if brand_ids and sub_sub_categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__sub_sub_categories_id__in=sub_sub_categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif brand_ids and sub_categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__sub_categories_id__in=sub_categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif brand_ids and categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__categories_id__in=categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif brand_ids:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    # elif brands_ids:
    #     category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands_ids).values_list('product__categories_id', flat=True).distinct()
    #     color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('color_id', flat=True).distinct()
    #     colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif sub_sub_categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_sub_categories_id__in=sub_sub_categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif sub_categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif categories:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    else:
        colors = admin_dashboard_models.Color.objects.all().values('id','name')

    return JsonResponse(list(colors), safe=False)

def get_sizes_from_color(request):
    brand_ids = request.GET.getlist('brand_ids[]')
    brands_ids = request.GET.getlist('brands_ids[]')
    color_ids = request.GET.getlist('color_ids[]')
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')

    if brand_ids and sub_sub_categories and color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__sub_sub_categories_id__in=sub_sub_categories, color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brand_ids and sub_categories and color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__sub_categories_id__in=sub_categories, color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif categories and brand_ids and color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories, product__product_varient__brand_id__in=brand_ids, color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_sub_categories and brand_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids, product__sub_sub_categories_id__in=sub_sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_sub_categories and color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_sub_categories_id__in=sub_sub_categories, color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_categories and color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories, color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_categories and brand_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories, product__product_varient__brand_id__in=brand_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif categories and brand_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories, product__product_varient__brand_id__in=brand_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif categories and color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories, color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brand_ids and color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids,color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brand_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__product_varient__brand_id__in=brand_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif brands_ids:
        category_ids = admin_dashboard_models.ProductVarient.objects.filter(brand_id__in=brands_ids).values_list('product__categories_id', flat=True).distinct()
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=category_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif color_ids:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(color_id__in=color_ids).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_sub_categories_id__in=sub_sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif sub_categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__sub_categories_id__in=sub_categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    elif categories:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(product__categories_id__in=categories).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id','value')
    else:
        sizes = admin_dashboard_models.Size.objects.all().values('id','value')

    return JsonResponse(list(sizes), safe=False)

# def get_colors_from_size(request):
#     size_ids = request.GET.getlist('size_ids[]')
#     if size_ids:
#         color_ids = admin_dashboard_models.ProductAttribute.objects.filter(size_id__in=size_ids).values_list('color_id', flat=True).distinct()
#         colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
#     else:
#         colors = admin_dashboard_models.Color.objects.all().values('id','name')

#     return JsonResponse(list(colors), safe=False)


# ajax for brand
def get_subcategories_from_category(request):
    categories = request.GET.getlist('categories[]')
    brand_id = request.GET.get('brand_id')

    if categories and brand_id:
        sub_categories = admin_dashboard_models.SubCategories.objects.filter(
            categories_id__in=categories,
            product_sub_categories__product_varient__brand_id=brand_id
        ).values('id', 'sub_cat_name').distinct()
    else:
        brand_product_qs = admin_dashboard_models.Product.objects.filter(product_varient__brand_id=brand_id)
        sub_category_ids = brand_product_qs.values_list('sub_categories_id', flat=True).distinct()
        sub_categories = admin_dashboard_models.SubCategories.objects.filter(id__in=sub_category_ids).values('id', 'sub_cat_name').distinct()

    return JsonResponse(list(sub_categories), safe=False)

def get_sub_sub_categories_from_category(request):
    categories = request.GET.getlist('categories[]')
    brand_id = request.GET.get('brand_id')

    if categories and brand_id:
        brand_product_qs = admin_dashboard_models.Product.objects.filter(product_varient__brand_id=brand_id)
        sub_sub_category_ids = brand_product_qs.values_list('sub_sub_categories_id', flat=True).distinct()
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(
            id__in=sub_sub_category_ids,
            sub_categories__categories_id__in=categories,
            sub_categories__product_sub_categories__product_varient__brand_id=brand_id
        ).values('id', 'sub_sub_cat_name').distinct()
    else:
        brand_product_qs = admin_dashboard_models.Product.objects.filter(product_varient__brand_id=brand_id)
        sub_sub_category_ids = brand_product_qs.values_list('sub_sub_categories_id', flat=True).distinct()
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(id__in=sub_sub_category_ids).values('id', 'sub_sub_cat_name').distinct()

    return JsonResponse(list(sub_sub_categories), safe=False)

def get_colors_from_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    brand_id = request.GET.get('brand_id')

    if categories and brand_id:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__product_varient__brand_id=brand_id
        ).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    else:
        colors = admin_dashboard_models.Color.objects.filter(product_color__product__product_varient__brand_id=brand_id).values('id', 'name').distinct()

    return JsonResponse(list(colors), safe=False)

def get_sizes_from_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    brand_id = request.GET.get('brand_id')

    if categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    else:
        sizes = admin_dashboard_models.Size.objects.filter(product_size__product__product_varient__brand_id=brand_id).values('id', 'value').distinct()

    return JsonResponse(list(sizes), safe=False)

def get_brands_from_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    brand_id = request.GET.get('brand_id')

    if categories and brand_id:
        brand_ids = admin_dashboard_models.ProductVarient.objects.filter(
            product__categories_id__in=categories,
            brand_id=brand_id
        ).values_list('brand_id', flat=True).distinct()
        brands = admin_dashboard_models.Brand.objects.filter(id__in=brand_ids).values('id','name')
    else:
        brands = admin_dashboard_models.Brand.objects.filter(id=brand_id).values('id','name')

    return JsonResponse(list(brands), safe=False)

# from sub category

def get_sub_sub_category_from_sub_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    brand_id = request.GET.get('brand_id')

    if sub_categories and brand_id:
        sub_sub_category_ids = admin_dashboard_models.Product.objects.filter(
            sub_categories_id__in=sub_categories,
            product_varient__brand_id=brand_id
        ).values_list('sub_sub_categories', flat=True).distinct()
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(id__in=sub_sub_category_ids).values('id', 'sub_sub_cat_name').distinct()
    elif categories and brand_id:
        sub_sub_category_ids = admin_dashboard_models.Product.objects.filter(
            categories_id__in=categories,
            product_varient__brand_id=brand_id
        ).values_list('sub_sub_categories', flat=True).distinct()
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(id__in=sub_sub_category_ids).values('id', 'sub_sub_cat_name').distinct()
    else:
        brand_product_qs = admin_dashboard_models.Product.objects.filter(product_varient__brand_id=brand_id)
        sub_sub_category_ids = brand_product_qs.values_list('sub_sub_categories_id', flat=True).distinct()
        sub_sub_categories = admin_dashboard_models.SubSubCategories.objects.filter(id__in=sub_sub_category_ids).values('id', 'sub_sub_cat_name').distinct()

    return JsonResponse(list(sub_sub_categories), safe=False)

def get_colors_from_sub_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    brand_id = request.GET.get('brand_id')

    if sub_categories and brand_id:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_categories_id__in=sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif categories and brand_id:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__product_varient__brand_id=brand_id
        ).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    else:
        colors = admin_dashboard_models.Color.objects.filter(product_color__product__product_varient__brand_id=brand_id).values('id', 'name').distinct()

    return JsonResponse(list(colors), safe=False)

def get_sizes_from_sub_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    brand_id = request.GET.get('brand_id')

    if sub_categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_categories_id__in=sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    elif categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    else:
        sizes = admin_dashboard_models.Size.objects.filter(product_size__product__product_varient__brand_id=brand_id).values('id', 'value').distinct()

    return JsonResponse(list(sizes), safe=False)

def get_colors_from_sub_sub_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    brand_id = request.GET.get('brand_id')

    if sub_sub_categories and brand_id:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_sub_categories_id__in=sub_sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif sub_categories and brand_id:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_categories_id__in=sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    elif categories and brand_id:
        color_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__product_varient__brand_id=brand_id
        ).values_list('color_id', flat=True).distinct()
        colors = admin_dashboard_models.Color.objects.filter(id__in=color_ids).values('id','name')
    else:
        colors = admin_dashboard_models.Color.objects.filter(product_color__product__product_varient__brand_id=brand_id).values('id', 'name').distinct()

    return JsonResponse(list(colors), safe=False)

def get_sizes_from_sub_sub_category_for_brand(request):
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    brand_id = request.GET.get('brand_id')

    if categories and sub_categories and sub_sub_categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__sub_categories_id__in=sub_categories,
            product__sub_sub_categories_id__in=sub_sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    
    elif categories and sub_categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__sub_categories_id__in=sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')

    elif sub_sub_categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_sub_categories_id__in=sub_sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    
    elif sub_categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_categories_id__in=sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
        
    elif categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    else:
        sizes = admin_dashboard_models.Size.objects.filter(product_size__product__product_varient__brand_id=brand_id).values('id', 'value').distinct()

    return JsonResponse(list(sizes), safe=False)

def get_sizes_from_color_for_brand(request):
    categories = request.GET.getlist('categories[]')
    sub_categories = request.GET.getlist('sub_categories[]')
    sub_sub_categories = request.GET.getlist('sub_sub_categories[]')
    color_ids = request.GET.getlist('color_ids[]')
    brand_id = request.GET.get('brand_id')

    if color_ids and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            color_id__in=color_ids,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    elif sub_sub_categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_sub_categories_id__in=sub_sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    elif sub_categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__sub_categories_id__in=sub_categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    elif categories and brand_id:
        size_ids = admin_dashboard_models.ProductAttribute.objects.filter(
            product__categories_id__in=categories,
            product__product_varient__brand_id=brand_id
        ).values_list('size_id', flat=True).distinct()
        sizes = admin_dashboard_models.Size.objects.filter(id__in=size_ids).values('id', 'value')
    else:
        sizes = admin_dashboard_models.Size.objects.filter(product_size__product__product_varient__brand_id=brand_id).values('id', 'value').distinct()

    return JsonResponse(list(sizes), safe=False)