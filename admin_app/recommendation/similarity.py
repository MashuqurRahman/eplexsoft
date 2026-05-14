import pandas as pd
from django.http import JsonResponse
from django.shortcuts import redirect, render
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from admin_app.models.admin_dashboard_models import (
    Product, ProductVarient, ProductAttribute
)
from .paths import SIM_PKL, SIM_CSV


def product_text(product):
    variants = ProductVarient.objects.filter(product=product)

    brands = " ".join(
        v.brand.name for v in variants if v.brand
    )

    colors = " ".join(
        attr.color.name
        for v in variants
        for attr in ProductAttribute.objects.filter(product_varient=v)
    )

    # new added
    category = product.categories.name if product.categories else ""
    sub_category = product.sub_categories.sub_cat_name if product.sub_categories else ""
    sub_sub_category = product.sub_sub_categories.sub_sub_cat_name if product.sub_sub_categories else ""

    return f"""
    {category}
    {sub_category}
    {sub_sub_category}
    {brands}
    {colors}
    {product.description or ''}
    """

    # return f"""
    # {product.categories.name}
    # {product.sub_categories.sub_cat_name}
    # {product.sub_sub_categories.sub_sub_cat_name}
    # {brands}
    # {colors}
    # {product.description or ''}
    # """


def build_similarity_matrix(request):
    try:
        if request.user.is_superuser or request.user.role == 'central_admin' or ("update_just_for_you_permission" in request.user.user_permissions and (request.user.role == 'section_admin' or request.user.role == 'employee')):
            products = Product.objects.all()
            ids, texts = [], []

            for p in products:
                ids.append(p.id)
                texts.append(product_text(p))

            tfidf = TfidfVectorizer(stop_words="english")
            matrix = tfidf.fit_transform(texts)

            cosine_sim = cosine_similarity(matrix)

            df = pd.DataFrame(cosine_sim, index=ids, columns=ids)
            df.to_pickle(SIM_PKL)
            df.to_csv(SIM_CSV)


            return redirect("admin_dashboard_url")
        else:
            return render(request, 'permission_denied.html')
    except:
        return render(request, 'permission_denied.html')