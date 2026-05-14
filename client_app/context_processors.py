from django.db.models import Sum, Prefetch
from admin_app.models import admin_dashboard_models

ACTIVE_MENU_URLS = [
    'category_products',
    'sub_category_products_shows_url',
    'products_page_url',
]

PRODUCT_DETAIL_URLS = [
    'product_details_page_url',
]

def categories_context(request):
    cart = None

    if request.user.is_authenticated:
        cart = admin_dashboard_models.Cart.objects.filter(user=request.user).first()
        wishlist = admin_dashboard_models.Wishlist.objects.filter(user=request.user)
        cart_items = admin_dashboard_models.CartItem.objects.prefetch_related('product__product_attribute').all()
    else:
        wishlist = admin_dashboard_models.Wishlist.objects.none()
        cart_items = admin_dashboard_models.CartItem.objects.none()
        session_key = request.session.session_key
        if session_key:
            cart = admin_dashboard_models.Cart.objects.filter(session_key=session_key).first()

    cart_items = cart.items.select_related('product', 'product_attribute', 'product__product_varient') if cart else []
    cart_quantity = cart.items.aggregate(total=Sum('quantity'))['total'] if cart else 0

    current_url = request.resolver_match.url_name if request.resolver_match else None
    current_category_id = None
    current_sub_category_id = None
    current_sub_sub_category_id = None

    if request.resolver_match:
        kwargs = request.resolver_match.kwargs
        url_name = request.resolver_match.url_name

        # ── Category / listing pages ──
        if url_name in ACTIVE_MENU_URLS:
            if 'category_id' in kwargs:
                current_category_id = kwargs.get('category_id')

            elif 'sub_cat_id' in kwargs:
                current_sub_category_id = kwargs.get('sub_cat_id')
                sub = admin_dashboard_models.SubCategories.objects.filter(
                    id=current_sub_category_id
                ).select_related('categories').first()
                if sub:
                    current_category_id = sub.categories.id

            elif 'pk' in kwargs:
                current_sub_sub_category_id = kwargs.get('pk')
                subsub = admin_dashboard_models.SubSubCategories.objects.filter(
                    id=current_sub_sub_category_id
                ).select_related('sub_categories__categories').first()
                if subsub:
                    current_sub_category_id = subsub.sub_categories.id
                    current_category_id = subsub.sub_categories.categories.id

        # ── Product detail page: trace category chain from product ──
        elif url_name in PRODUCT_DETAIL_URLS:
            product_pk = kwargs.get('pk') or kwargs.get('id') or kwargs.get('product_id')
            if product_pk:
                product = admin_dashboard_models.Product.objects.filter(
                    id=product_pk
                ).select_related(
                    'sub_sub_categories__sub_categories__categories',
                    'sub_categories__categories'
                ).first()

                if product and product.sub_sub_categories:
                    subsub = product.sub_sub_categories
                    current_sub_sub_category_id = subsub.id
                    current_sub_category_id = subsub.sub_categories.id
                    current_category_id = subsub.sub_categories.categories.id
                elif product and product.sub_categories:
                    current_sub_category_id = product.sub_categories.id
                    current_category_id = product.sub_categories.categories.id



    categories = admin_dashboard_models.Categories.objects.prefetch_related(
        Prefetch(
            'sub_categories',
            queryset=admin_dashboard_models.SubCategories.objects.order_by('column', 'position').prefetch_related(
                'sub_sub_categories'
            )
        )
    ).all()

    return {
        # 'categories': admin_dashboard_models.Categories.objects.prefetch_related(
        #     'sub_categories__sub_sub_categories__product_sub_sub_categories'
        # ),
        'categories': categories,
        'sub_categories_one': admin_dashboard_models.SubCategories.objects.filter(column=1).order_by('position'),
        'cart_items': cart_items,
        'wish_list': wishlist,
        'cart_quantity': cart_quantity,
        'current_url': current_url,
        'current_category_id': current_category_id,
        'current_sub_category_id': current_sub_category_id,
        'current_sub_sub_category_id': current_sub_sub_category_id,
    }



def site_settings(request):
    setting = admin_dashboard_models.SiteSetting.objects.filter(is_active=True).first()
    payment_logos = admin_dashboard_models.paymentMethodLogos.objects.all()
    return {
        'site_setting': setting,
        'payment_logos': payment_logos
    }

def theme_colors(request):
    theme = admin_dashboard_models.ClientThemeSetting.objects.first()
    return {
        'FOOTER_COLOR': theme.footer_color if theme else "#761731",
        'NOTIFICATION_COLOR': theme.notification_color if theme else "#EF4444",
        'PRICE_COLOR': theme.price_color if theme else "#EF4444",
        'BUTTON_COLOR': theme.button_color if theme else "#EB2E61"
    }


def auth_errors_processor(request):
    auth_errors = request.session.pop("auth_errors", None)
    if auth_errors:
        return auth_errors
    return {}