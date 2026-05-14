import re
from unicodedata import category
from rapidfuzz import fuzz, process
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from requests import request
from difflib import SequenceMatcher
from admin_app.models import admin_dashboard_models
from django.db.models import Avg, Count, DecimalField, Prefetch, Min, F, Value, Q
from django.db.models.functions import Coalesce, Random, Replace, Lower
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from client_app.models import client_models
import pickle
import numpy as np
import pandas as pd

PRODUCT_LIMIT = 10
SIMILARITY_PKL_PATH = "product_similarity.pkl"

def load_similarity_matrix():
    try:
        df = pd.read_pickle(SIMILARITY_PKL_PATH)
        # df: index=product_id, columns=product_id
        return df
    except Exception as e:
        print("Similarity matrix load failed:", e)
        return None



def get_home_page_context(request):
    context = {}
    is_search = request.GET.get('is_search')

    if request.user.is_authenticated:
        user_wishlist_ids = admin_dashboard_models.Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        user_wishlist_ids = admin_dashboard_models.Wishlist.objects.all().values_list('product_id', flat=True)
    obj_list = admin_dashboard_models.Product.objects.all()
    #products = admin_dashboard_models.Product.objects.prefetch_related('product_varient').filter(product_varient__status='active').order_by('-id')[:PRODUCT_LIMIT]
    #popular_products = admin_dashboard_models.Product.objects.prefetch_related('product_varient', 'product_attribute').filter(product_varient__status='active', is_popular=True).order_by('-id')[:PRODUCT_LIMIT]

    flash_sale_product_ids = admin_dashboard_models.FlashSell.objects.filter(side_slider__campaign_type="flash_sale",side_slider__in= admin_dashboard_models.SideSlider.objects.all()).values_list('product', flat=True)


    flash_sale_product_obj = admin_dashboard_models.Product.objects.filter(id__in=list(flash_sale_product_ids)).order_by('-id')[:10]
    products = (
        admin_dashboard_models.Product.objects
        .filter(
            is_active=True,
        )
        .prefetch_related(
            Prefetch(
                'product_attribute',
                queryset=admin_dashboard_models.ProductAttribute.objects.all()
            )
        ).order_by('-id')
        .distinct()[:10]
    )
    popular_products = (
        admin_dashboard_models.Product.objects
        .filter(
            is_active=True,
            is_popular=True
        )
        .prefetch_related(
            Prefetch(
                'product_attribute',
                queryset=admin_dashboard_models.ProductAttribute.objects.all()
            )
        ).order_by('-id')
        .distinct()[:10]
        
    )

    best_deal_products = (
        admin_dashboard_models.Product.objects
        .filter(
            is_active=True,
            is_best_deal=True
        )
        .prefetch_related(
            Prefetch(
                'product_attribute',
                queryset=admin_dashboard_models.ProductAttribute.objects.all()
            )
        ).order_by('-id')
        .distinct()[:10]
        
    )

    # -------------------------------
    # JUST FOR YOU (Ranked by user view history)
    # -------------------------------

    just_for_you_products = []

    if request.user.is_authenticated:

        top_viewed = (
            admin_dashboard_models.RecentlyViewedProduct.objects
            .filter(user=request.user)
            .select_related('product')
            .order_by('-view_count')
        )

        num_views = top_viewed.count()


        if num_views == 0:
            just_for_you_products = popular_products[:PRODUCT_LIMIT]

        else:
            sim_df = load_similarity_matrix()

            if sim_df is None:
                just_for_you_products = popular_products[:PRODUCT_LIMIT]

            else:
                scores = {}

                for rv in top_viewed:
                    pid = rv.product_id

                    if pid in sim_df.index:
                        for target_pid, sim_value in sim_df.loc[pid].items():
                            scores[target_pid] = scores.get(target_pid, 0) + (
                                sim_value * rv.view_count
                            )

                ranked_product_ids = sorted(
                    scores.keys(),
                    key=lambda x: scores[x],
                    reverse=True
                )

                just_for_you_products = (
                    admin_dashboard_models.Product.objects
                    .filter(
                        id__in=ranked_product_ids,
                        is_active=True
                    )
                    .distinct()
                )

                just_for_you_products = sorted(
                    just_for_you_products,
                    key=lambda p: ranked_product_ids.index(p.id)
                )[:PRODUCT_LIMIT]


            

    else:
        just_for_you_products = popular_products[:PRODUCT_LIMIT]



   

    categories = (
        admin_dashboard_models.Categories.objects.all().order_by('-id')
        .order_by('name')
    )
    hero_sliders =  admin_dashboard_models.Slider.objects.filter(is_active=True).order_by('-created_at')
    side_sliders =  admin_dashboard_models.SideSlider.objects.filter(campaign_type='campaign').order_by('-created_at')[:2]

    first_slider = side_sliders[0] if len(side_sliders) > 0 else None
    second_slider = side_sliders[1] if len(side_sliders) > 1 else None
    
    
   
    context.update({
        'obj_list': obj_list,
        'products':products,
        'popular_products':popular_products,
        'best_deal_products':best_deal_products,
        'categories': categories,
        'hero_sliders': hero_sliders,
        # 'side_sliders': side_sliders,
        'first_slider': first_slider,
        'second_slider': second_slider,
        'user_wishlist_ids': user_wishlist_ids,
        # 'flashsell_products': flashsell_products,
        'flashsell_products': flash_sale_product_obj,
        'just_for_you_products': just_for_you_products,
        # 'flash_sale_product_obj': flash_sale_product_obj,
    })
    return context

def home_page_view(request):
    context = get_home_page_context(request)
    return render(request, 'client/home.html', context)

def load_more_products(request):
    offset = int(request.GET.get('offset', 0))

    products = (
        admin_dashboard_models.Product.objects
        .filter(
            is_active=True
        )
        .prefetch_related(
            Prefetch(
                'product_attribute',
                queryset=admin_dashboard_models.ProductAttribute.objects.all()
            )
        ).order_by('-id')[offset:offset + PRODUCT_LIMIT]  
    )

    just_for_you_products = []

    if request.user.is_authenticated:

        top_viewed = (
            admin_dashboard_models.RecentlyViewedProduct.objects
            .filter(user=request.user)
            .select_related('product')
            .order_by('-view_count')
        )

        num_views = top_viewed.count()


        if num_views == 0:
            just_for_you_products = products[offset:offset + PRODUCT_LIMIT]

        else:
            sim_df = load_similarity_matrix()

            if sim_df is None:
                just_for_you_products = products[offset:offset + PRODUCT_LIMIT]

            else:
                scores = {}

                for rv in top_viewed:
                    pid = rv.product_id

                    if pid in sim_df.index:
                        for target_pid, sim_value in sim_df.loc[pid].items():
                            scores[target_pid] = scores.get(target_pid, 0) + (
                                sim_value * rv.view_count
                            )

                ranked_product_ids = sorted(
                    scores.keys(),
                    key=lambda x: scores[x],
                    reverse=True
                )

                just_for_you_products = (
                    admin_dashboard_models.Product.objects
                    .filter(
                        id__in=ranked_product_ids,
                        is_active = True
                    )
                    .distinct()
                )

                just_for_you_products = sorted(
                    just_for_you_products,
                    key=lambda p: ranked_product_ids.index(p.id)
                )[offset:offset + PRODUCT_LIMIT]

    else:
        just_for_you_products = products
        

    html = render_to_string(
        'client/products/product_card.html',
        {'just_for_you_products': just_for_you_products}
    )
    return JsonResponse({
        'html': html,
        'has_more': products.count() == PRODUCT_LIMIT
    })

# def products_page_view(request, pk):
#     if request.user.is_authenticated:
#         user_wishlist_ids = admin_dashboard_models.Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
#     else:
#         user_wishlist_ids = admin_dashboard_models.Wishlist.objects.all().values_list('product_id', flat=True)

#     breadcrumbs = [
#         {'name': 'Home', 'url': reverse('home_page_url')},
#         {'name': 'Products', 'url': None},
#     ]
  
#     products_obj = (
#         admin_dashboard_models.Product.objects
#         .filter(
#             sub_sub_categories__id=pk,
#             is_active=True,
#         )
#         .prefetch_related(
#             Prefetch(
#                 'product_attribute',
#                 queryset=admin_dashboard_models.ProductAttribute.objects.filter(is_cover=True)
#             )
#         )
#         .distinct()
#     )
    
#     page = request.GET.get('page')
#     paginator = Paginator(products_obj, 10)
#     try:
#         products_obj = paginator.page(page)
#     except PageNotAnInteger:
#         products_obj = paginator.page(1)
#     except EmptyPage:
#         products_obj = paginator.page(paginator.num_pages)

#     context = {
#         'obj_list': products_obj,
#         'user_wishlist_ids': user_wishlist_ids,
#         'breadcrumbs': breadcrumbs
#     }
#     return render(request, 'client/products/products.html', context)

def products_page_view(request, pk):
    sub_sub_category = get_object_or_404(admin_dashboard_models.SubSubCategories, id=pk)
    sub_category = sub_sub_category.sub_categories
    category_id = sub_category.categories.id

    products = (
        admin_dashboard_models.Product.objects
        .filter(is_active=True)
        .prefetch_related(
            Prefetch(
                'product_attribute',
                queryset=admin_dashboard_models.ProductAttribute.objects.filter(is_cover=True)
            )
        )
        .select_related('product_varient')
        .order_by('-id')
    )
    
    # products = (
    #     admin_dashboard_models.Product.objects
    #     .filter(
    #         sub_sub_categories__id=pk,
    #         is_active=True,
    #     )
    #     .prefetch_related(
    #         Prefetch(
    #             'product_attribute',
    #             queryset=admin_dashboard_models.ProductAttribute.objects.filter(is_cover=True)
    #         )
    #     )
    #     .distinct()
    # )
    
    sub_sub_category = get_object_or_404(admin_dashboard_models.SubSubCategories, id=pk)
    sub_category = sub_sub_category.sub_categories
    category_id = sub_category.categories.id

    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.filter(categories=category_id)
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id=category_id)
    brands_obj = admin_dashboard_models.Brand.objects.filter(product_brand__product__categories_id=category_id).distinct()
    # colors_obj = admin_dashboard_models.Color.objects.filter(product_color__product__sub_sub_categories_id=sub_sub_category.id).distinct()
    colors_obj = admin_dashboard_models.Color.objects.filter(product_color__product__categories_id=category_id).distinct()
    sizes_obj = admin_dashboard_models.Size.objects.filter(product_size__product__categories_id=category_id).distinct()
    # sizes_obj = admin_dashboard_models.Size.objects.filter(product_size__product__sub_sub_categories_id=sub_sub_category.id).distinct()

    if not categories and not sub_categories and not sub_sub_categories:
        products = products.filter(sub_sub_categories__id=pk)
        
    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')
    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')
    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        "products": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "category": category_id,
        "sub_category": sub_category,
        "sub_sub_category": sub_sub_category,
        "is_subsubcategory": True,
        'page_title': 'Sub Sub Category Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/common.html',
            context
        )

    return render(
        request,
        'client/filter/categories_products.html',
        context
    )


def products_details_page_view(request, pk):
    product = admin_dashboard_models.Product.objects.get(id=pk)
    if product.sub_sub_categories_id:
        similar_product_obj = admin_dashboard_models.Product.objects.filter(
            sub_sub_categories_id=product.sub_sub_categories_id
        ).prefetch_related('product_varient').exclude(id=pk)
    else:
        similar_product_obj = admin_dashboard_models.Product.objects.filter(
            sub_categories_id=product.sub_categories_id
        ).prefetch_related('product_varient').exclude(id=pk)
    # Review Rating logic

    reviews = client_models.ReviewRating.objects.filter(product=product)
    selected_review = reviews.filter(is_selected=True)

    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    rounded = round(avg_rating * 2) / 2  
    full_stars = int(rounded)
    half_star = 1 if rounded - full_stars == 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    for review in selected_review:
        review.fullstar = int(review.rating)
 
    
    delivery_charge = []
    if request.user.is_authenticated:
        user_wishlist_ids = admin_dashboard_models.Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

        #-------------------
        # NJA Added to count View
        #--------------------
        obj, created = admin_dashboard_models.RecentlyViewedProduct.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'viewed_at': timezone.now()},
        )

        if not created:
            # increment view_count atomically
            admin_dashboard_models.RecentlyViewedProduct.objects.filter(
                id=obj.id
            ).update(view_count=F('view_count') + 1)   

        #-------------------
        # End
        #--------------------


        #admin_dashboard_models.RecentlyViewedProduct.objects.update_or_create(user=request.user, product=product)
        recent_qs = admin_dashboard_models.RecentlyViewedProduct.objects.filter(user=request.user).order_by('-viewed_at')
        ids_to_delete = list(recent_qs.values_list('id', flat=True)[10:])

        admin_dashboard_models.RecentlyViewedProduct.objects.filter(
            id__in=ids_to_delete
        ).delete()
        #admin_dashboard_models.RecentlyViewedProduct.objects.filter(user=request.user).order_by('-viewed_at')[10:].delete()
    else:
        user_wishlist_ids = admin_dashboard_models.Wishlist.objects.all().values_list('product_id', flat=True)


    try:
        sub_sub_cat = get_object_or_404(admin_dashboard_models.SubSubCategoryDeliveryCharge, sub_sub_category=product.sub_sub_categories)
        delivery_charge = get_object_or_404(admin_dashboard_models.DeliveryCharge, id=sub_sub_cat.delivery_charge.id)


    except:
        pass

    popular_products = (
        admin_dashboard_models.Product.objects
        .filter(
            is_active=True,
            is_popular=True
        )
        .prefetch_related(
            'product_varient',
            Prefetch(
                'product_attribute',
                queryset=admin_dashboard_models.ProductAttribute.objects.filter(is_cover=True)
            )
        )
        .order_by('-id')[:10]
    )
    product_obj = admin_dashboard_models.ProductVarient.objects.select_related('product').prefetch_related('product__product_attribute').get(product__id=pk)
    attribute_list = admin_dashboard_models.ProductAttribute.objects.filter(product_varient=product_obj.id)
    attribute_obj = admin_dashboard_models.ProductAttribute.objects.filter(product=product.id).prefetch_related('product_attribute_image').first()

    distinct_colors = attribute_list.values('color__id', 'color__name').distinct()
    distinct_sizes = attribute_list.values('size__id', 'size__value').distinct()
    breadcrumbs = [
        {'name': "Home", 'url': reverse('home_page_url')},
        {'name': "Products", 'url': reverse('products_page_url', args=[product_obj.product.sub_categories.id])},
        {'name': product_obj.product.product_name, 'url': None},
    ]
    context = {
        'delivery_charge': delivery_charge,
        'product': product_obj,
        'popular_products': popular_products,
        'attribute_list': attribute_list,
        'colors': distinct_colors,
        'sizes': distinct_sizes,
        'breadcrumbs': breadcrumbs,
        'user_wishlist_ids': user_wishlist_ids,
        'similar_product_obj': similar_product_obj,
        'product_obj': product,
        'attribute_obj': attribute_obj,
        
        "full_stars": range(full_stars),
        "half_star": half_star,
        "empty_stars": range(empty_stars),
        "selected_reviews": selected_review,
        "see_more_reviews": selected_review.count() > 1
    }
    return render(request, 'client/products/product_details.html', context)

def digital_products_page_view(request):
    return render(request, 'client/digital-products.html')

# Review Rating View
@login_required
def submit_review_view(request):

    if request.method == "POST":

        product_id = request.POST.get("product_id")
        rating = request.POST.get("rating")
        review = request.POST.get("review")

        product = admin_dashboard_models.Product.objects.get(id=product_id)

        client_models.ReviewRating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'review': review
            }
        )

        return JsonResponse({"success":True})


def category_products(request, category_id=None):
    category = None
    products, category = [], []
    product_qs = admin_dashboard_models.Product.objects.prefetch_related(
        Prefetch(
            'product_varient',
            queryset=admin_dashboard_models.ProductVarient.objects.all(),
            to_attr='active_variants'
        )
    ).filter(is_active=True).order_by('-id')

    if category_id:
        category = get_object_or_404(
            admin_dashboard_models.Categories,
            id=category_id
        )
        sub_category = admin_dashboard_models.SubCategories.objects.filter(categories_id=category_id).first()
        products = product_qs.filter(categories_id=category_id)



    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.filter(categories_id=category_id)
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id=category_id)
    brands_obj = admin_dashboard_models.Brand.objects.filter(product_brand__product__categories_id=category_id).distinct()
    colors_obj = admin_dashboard_models.Color.objects.filter(product_color__product__categories_id=category_id).distinct()
    sizes_obj = admin_dashboard_models.Size.objects.filter(product_size__product__categories_id=category_id).distinct()

    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')
    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')
    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        "products": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "category": category.id,
        "category_obj": category,
        "sub_category": sub_category,
        "is_category": True,
        'page_title': 'Category Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/common.html',
            context
        )

    return render(
        request,
        'client/filter/categories_products.html',
        context
    )


def most_popular_products(request):
    products = admin_dashboard_models.Product.objects.filter(
        is_popular=True,
        is_active=True
    )


    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.all()
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.all()
    brands_obj = admin_dashboard_models.Brand.objects.all()
    colors_obj = admin_dashboard_models.Color.objects.all()
    sizes_obj = admin_dashboard_models.Size.objects.all()

    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')

    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')

    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        "products": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "is_popular": True,
        'page_title': 'Most Popular Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/popular_product.html',
            context
        )

    return render(
        request,
        'client/filter/filter_base.html',
        context
    )
    
def best_deal_products(request):
    products = admin_dashboard_models.Product.objects.filter(
        is_best_deal=True,
        is_active=True,
    ).order_by('-id')


    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.all()
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.all()
    brands_obj = admin_dashboard_models.Brand.objects.all()
    colors_obj = admin_dashboard_models.Color.objects.all()
    sizes_obj = admin_dashboard_models.Size.objects.all()

    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')
    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')
    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')


    context = {
        "products": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "is_best_deal": True,
        'page_title': 'Best Deal Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/best_deal.html',
            context
        )

    return render(
        request,
        'client/filter/filter_base.html',
        context
    )


def flash_sell_products(request):
    flashsale_ids = admin_dashboard_models.FlashSell.objects.filter(side_slider__campaign_type='flash_sale', product__is_active=True).values_list('product', flat=True)
    products = admin_dashboard_models.Product.objects.filter(id__in=list(flashsale_ids)).prefetch_related('product_attribute').select_related('product_varient').order_by('-id')

    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.all()
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.all()
    brands_obj = admin_dashboard_models.Brand.objects.all()
    colors_obj = admin_dashboard_models.Color.objects.all()
    sizes_obj = admin_dashboard_models.Size.objects.all()

    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()
    
    if sort_by == 'most_recent':
        products = products.order_by('-created_at')
    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')
    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')


    context = {
        "products": products,
        "flash_sell_product": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "is_flash_sale": True,
        'page_title': 'Flash Sale Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/flash_sale.html',
            context
        )

    return render(
        request,
        'client/filter/filter_base.html',
        context
    )



def brand_wise_products_view(request, brand_id):
    brand = admin_dashboard_models.Brand.objects.get(id=brand_id)

    products = admin_dashboard_models.Product.objects.prefetch_related(
        'product_attribute'
    ).filter(
        product_varient__brand_id=brand_id
    ).order_by('-id')

    brand_product_qs = admin_dashboard_models.Product.objects.filter(
        product_varient__brand_id=brand_id
    )

    sub_category_ids = brand_product_qs.values_list('sub_categories_id', flat=True).distinct()
    sub_sub_cat_ids = brand_product_qs.values_list('sub_sub_categories_id', flat=True).distinct()

    sub_sub_category = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories_id__in=sub_category_ids)
    sub_category = admin_dashboard_models.SubCategories.objects.filter(id__in=sub_category_ids)
    category_id = sub_category.values_list('categories_id', flat=True)

    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.filter(id__in=list(category_id))
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.filter(id__in=sub_category_ids)
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.filter(id__in=sub_sub_cat_ids)
    brands_obj = admin_dashboard_models.Brand.objects.filter(id=brand_id)
    colors_obj = admin_dashboard_models.Color.objects.filter(product_color__product__product_varient__brand_id=brand_id).distinct()
    sizes_obj = admin_dashboard_models.Size.objects.filter(product_size__product__product_varient__brand_id=brand_id).distinct()

    
    if not categories and not sub_categories and not sub_sub_categories:
        products = products.filter(product_varient__brand_id=brand_id)
    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')
    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')
    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')
    
    

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    

    context = {
        "brand": brand,
        "products": products,
        "categoriess": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "category": category_id,
        "sub_category": sub_category,
        "sub_sub_category": sub_sub_category,
        "is_brand": True,
        'page_title': 'Brand wise Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/common.html',
            context
        )

    return render(
        request,
        'client/filter/brand_filter_base.html',
        context
    )


def campaign_products_view(request, campaign_id):
    campaign_id = admin_dashboard_models.SideSlider.objects.get(id=campaign_id)
    campaign_product_ids = admin_dashboard_models.FlashSell.objects.filter(side_slider__campaign_type="campaign",side_slider=campaign_id).values_list('product', flat=True)
    products = admin_dashboard_models.Product.objects.filter(id__in=list(campaign_product_ids))

    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.all()
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.all()
    brands_obj = admin_dashboard_models.Brand.objects.all()
    colors_obj = admin_dashboard_models.Color.objects.all()
    sizes_obj = admin_dashboard_models.Size.objects.all()

    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')
    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')
    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')


    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')


    context = {
        "products": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        'campaign':campaign_id,
        "is_campaign": True,
        'page_title': 'Campaign Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,

    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/campaign_products.html',
            context
        )

    return render(
        request,
        'client/filter/filter_base.html',
        context
    )



def categories_list(request):

    categories_qs = admin_dashboard_models.Categories.objects.all().order_by('-id')

    paginator = Paginator(categories_qs , 10)
    page_number = request.GET.get('page')
    categories_qs  = paginator.get_page(page_number)

    context = {
        'categories_qs': categories_qs,
        'page_title': 'Categories',
    }

    return render(request, 'client/categories/categories.html', context)


def product_search_view(request):
    search_words = request.GET.get('search', '').strip()

    def clean_text(text):
        return ' '.join(re.sub(r'[^a-zA-Z0-9\s]', ' ', text).split())

    def words_mostly_match(query, field_value, match_ratio=0.5):
        query_words = clean_text(query).lower().split()
        field_words = clean_text(field_value).lower().split()

        if not query_words:
            return False

        matched = 0
        for q_word in query_words:
            best = max(
                (fuzz.ratio(q_word, f_word) for f_word in field_words),
                default=0
            )
            if best >= 70:
                matched += 1

        return (matched / len(query_words)) >= match_ratio

    def score_field(query, field_value):
        q = clean_text(query).lower()
        f = clean_text(field_value).lower()

        query_words = q.split()
        field_words = f.split()

        word_scores = []
        for q_word in query_words:
            best = max(
                (fuzz.ratio(q_word, f_word) for f_word in field_words),
                default=0
            )
            word_scores.append(best)

        if not word_scores:
            return 0

        avg_word_score = sum(word_scores) / len(word_scores)

        if avg_word_score < 40:
            return 0

        exact_bonus = 15 if q in f else 0
        all_matched_bonus = 10 if all(s >= 75 for s in word_scores) else 0

        return avg_word_score + exact_bonus + all_matched_bonus

    def score_product(product, phrases):
        product_name = product.product_name or ""
        category = product.categories.name if product.categories else ""
        sub_cat = product.sub_categories.sub_cat_name if product.sub_categories else ""
        sub_sub_cat = product.sub_sub_categories.sub_sub_cat_name if product.sub_sub_categories else ""

        fields = [
            (product_name, 1.5),
            (category, 1.2),
            (sub_cat, 1.1),
            (sub_sub_cat, 1.0),
        ]

        best_score = 0

        for phrase in phrases:
            for field_value, weight in fields:
                if not words_mostly_match(phrase, field_value, match_ratio=0.7):
                    continue

                raw = score_field(phrase, field_value)
                if raw > 0:
                    weighted = raw * weight
                    if weighted > best_score:
                        best_score = weighted

        return best_score

    raw_phrases = search_words.split(',')
    phrases = [clean_text(p) for p in raw_phrases if clean_text(p)]

    if not phrases:
        context = {'search_words': search_words, 'products': []}
        return render(request, 'client/search_products/search.html', context)

    all_products = list(admin_dashboard_models.Product.objects.select_related('categories', 'sub_categories', 'sub_sub_categories'))

    scored_products = [(product, score_product(product, phrases))for product in all_products]
    final_products = [product for product, score in sorted(scored_products, key=lambda x: x[1], reverse=True) if score > 0]

    context = {
        'search_words': search_words,
        'products': final_products
    }

    return render(request, 'client/search_products/search.html', context)


def sub_category_product_show_view(request, sub_cat_id):
    sub_category = None
    products, sub_category = [], []

    sub_category = get_object_or_404(admin_dashboard_models.SubCategories,id=sub_cat_id)
    category_id = sub_category.categories.id

    
    product_qs = admin_dashboard_models.Product.objects.prefetch_related(
        Prefetch(
            'product_varient',
            queryset=admin_dashboard_models.ProductVarient.objects.all(),
            to_attr='active_variants'
        )
    ).filter(is_active=True).order_by('-id')

    products = product_qs
    

    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.filter(categories=category_id)
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__categories_id=category_id)
    brands_obj = admin_dashboard_models.Brand.objects.filter(product_brand__product__categories_id=category_id).distinct()
    # colors_obj = admin_dashboard_models.Color.objects.filter(product_color__product__sub_categories_id=sub_category.id).distinct()
    colors_obj = admin_dashboard_models.Color.objects.filter(product_color__product__categories_id=category_id).distinct()
    sizes_obj = admin_dashboard_models.Size.objects.filter(product_size__product__categories_id=category_id).distinct()
    # sizes_obj = admin_dashboard_models.Size.objects.filter(product_size__product__sub_categories_id=sub_category.id).distinct()

    if not categories and not sub_categories:
        products = products.filter(sub_categories_id=sub_cat_id)

    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes)|
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories,product_attribute__size_id__in=sizes)
        )


    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')
    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        if sort_by == 'price_high_to_low':
            products = products.order_by('-sort_price')
        else:
            products = products.order_by('sort_price')
    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')


    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        "products": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "category": category_id,
        "sub_category": sub_category,
        "is_subcategory": True,
        'page_title': 'Sub Category Products',

        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'client/filter/common.html',
            context
        )

    return render(
        request,
        'client/filter/categories_products.html',
        context
    )

def just_for_you_products_show_view(request):
    popular_products = (
        admin_dashboard_models.Product.objects
        .filter(is_active=True, is_popular=True)
        .prefetch_related(
            Prefetch(
                'product_attribute',
                queryset=admin_dashboard_models.ProductAttribute.objects.all()
            )
        ).order_by('-id')
        .distinct()
    )

    just_for_you_product_ids = None  

    if request.user.is_authenticated:
        top_viewed = (
            admin_dashboard_models.RecentlyViewedProduct.objects
            .filter(user=request.user)
            .select_related('product')
            .order_by('-view_count')
        )

        num_views = top_viewed.count()

        if num_views > 0:
            sim_df = load_similarity_matrix()

            if sim_df is not None:
                scores = {}

                for rv in top_viewed:
                    pid = rv.product_id
                    if pid in sim_df.index:
                        for target_pid, sim_value in sim_df.loc[pid].items():
                            scores[target_pid] = scores.get(target_pid, 0) + (
                                sim_value * rv.view_count
                            )

                ranked_product_ids = sorted(
                    scores.keys(),
                    key=lambda x: scores[x],
                    reverse=True
                )

                just_for_you_product_ids = ranked_product_ids  


    if just_for_you_product_ids is not None:
        products = (
            admin_dashboard_models.Product.objects
            .filter(id__in=just_for_you_product_ids, is_active=True)
            .distinct()
        )
    else:
        products = (
            admin_dashboard_models.Product.objects
            .filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    'product_attribute',
                    queryset=admin_dashboard_models.ProductAttribute.objects.all()
                )
            ).order_by('-id')
            .distinct()
        )

    categories = request.GET.getlist('category')
    sub_categories = request.GET.getlist('sub_category')
    sub_sub_categories = request.GET.getlist('sub_sub_category')
    brands = request.GET.getlist('brand')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'default')

    categories_obj = admin_dashboard_models.Categories.objects.all()
    sub_categories_obj = admin_dashboard_models.SubCategories.objects.all()
    sub_sub_categories_obj = admin_dashboard_models.SubSubCategories.objects.all()
    brands_obj = admin_dashboard_models.Brand.objects.all()
    colors_obj = admin_dashboard_models.Color.objects.all()
    sizes_obj = admin_dashboard_models.Size.objects.all()

    if categories:
        products = products.filter(categories_id__in=categories)

    if sub_categories:
        products = (
            products.filter(sub_categories_id__in=sub_categories) |
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories)
        )

    if sub_sub_categories:
        products = (
            products.filter(sub_sub_categories_id__in=sub_sub_categories) |
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories)
        )

    if brands:
        products = (
            products.filter(product_varient__brand_id__in=brands) |
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories, product_varient__brand_id__in=brands)
        )

    if colors:
        products = (
            products.filter(product_attribute__color_id__in=colors) |
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories, product_attribute__color_id__in=colors)
        )

    if sizes:
        products = (
            products.filter(product_attribute__size_id__in=sizes) |
            products.filter(categories_id__in=categories, sub_categories_id__in=sub_categories, sub_sub_categories_id__in=sub_sub_categories, product_attribute__size_id__in=sizes)
        )

    if min_price:
        products = products.filter(product_attribute__final_price__gte=min_price)
    if max_price:
        products = products.filter(product_attribute__final_price__lte=max_price)

    if min_price and max_price and min_price == max_price:
        products = products.filter(product_attribute__final_price=min_price)

    if min_price and max_price and min_price < max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    if min_price and max_price and min_price > max_price:
        products = (
            products.filter(product_attribute__final_price__gte=min_price, product_attribute__final_price__lte=max_price)
        )

    products = products.distinct()

    if sort_by == 'most_recent':
        products = products.order_by('-created_at')

    elif sort_by in ('price_high_to_low', 'price_low_to_high'):
        products = products.annotate(
            sort_price=Coalesce(
                F('cover_product_attribute__final_price'),
                F('cover_product_attribute__discount_price'),
                F('cover_product_attribute__regular_price'),
                output_field=DecimalField()
            )
        )
        products = products.order_by('-sort_price' if sort_by == 'price_high_to_low' else 'sort_price')

    elif sort_by == 'name_a_to_z':
        products = products.order_by('product_name')
    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')


    elif just_for_you_product_ids and sort_by == 'default':
        id_order = {pid: idx for idx, pid in enumerate(just_for_you_product_ids)}
        products = sorted(products, key=lambda p: id_order.get(p.id, 9999))



    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        "products": products,
        "categories": categories_obj,
        "sub_categories": sub_categories_obj,
        "sub_sub_categories": sub_sub_categories_obj,
        "brands": brands_obj,
        "colors": colors_obj,
        "sizes": sizes_obj,
        "is_popular": True,
        "is_just_for_you": True,
        'page_title': 'Just For You',
        "query_params": query_params.urlencode(),
        "selected_categories": categories,
        "selected_sub_categories": sub_categories,
        "selected_sub_sub_categories": sub_sub_categories,
        "selected_brands": brands,
        "selected_colors": colors,
        "selected_sizes": sizes,
        "sort_by": sort_by,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'client/filter/just_for_you.html', context)

    return render(request, 'client/filter/filter_base.html', context)

    

# AJAX
def get_variant_data(request):
    variant_id = request.GET.get('variant_id')
    color_id = request.GET.get('color_id')
    size_id = request.GET.get('size_id')

    try:
        attribute = admin_dashboard_models.ProductAttribute.objects.prefetch_related('product_attribute_image').get(
            product_varient_id=variant_id,
            color_id=color_id,
            size_id=size_id
        )

        images = attribute.product_attribute_image.all()
        image_list = []
        if attribute.image:
            image_list.append({
                'id': 'main_image',
                'url': attribute.image.url
            })
        if images.exists():
            for img in images:
                image_list.append({
                    'id': img.id,
                    'url': img.image.url
                })
        else:
            fallback_image = admin_dashboard_models.ProductAttributeImage.objects.filter(product_attribute__product_varient_id=variant_id).order_by(Random())[:5]
            for img in fallback_image:
                image_list.append({
                    'id': img.id,
                    'url': img.image.url
                })
       
        data = {
            'success': True,
            'image_url': attribute.image.url,
            'regular_price': str(attribute.regular_price),
            'discount_price': attribute.product_final_price,
            'discount_percent': attribute.final_discount['total_discount_percentage'],
            'stock_qty': attribute.attribute_stock_status["remaining_stock"],
            'stock_status':attribute.attribute_stock_status["status"],
            'attribute_id': attribute.id,
            'primary_image': attribute.image.url if attribute.image else None,
            'gallery_images': image_list
        }
    except admin_dashboard_models.ProductAttribute.DoesNotExist:
        data = {'success': False, 'message': 'Combination not available'}

    return JsonResponse(data)