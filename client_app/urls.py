from django.urls import path
from .views import main_menu_views, footer_views, cart_wishlist_views, user_dashboard_views, theme_setting_views, filter_views

urlpatterns = [
    path('', main_menu_views.home_page_view, name='home_page_url'),
    path('load-more/', main_menu_views.load_more_products, name='load_more_products'),
    path('category/<int:category_id>/',main_menu_views.category_products, name='category_products'),
    path('products/',main_menu_views.category_products, name='all_products'),
    path('products/popular/',main_menu_views.most_popular_products,name='most_popular_products'),
    path('products/best-deal/',main_menu_views.best_deal_products,name='best_deal_products'),
    path('products/flash-sale/',main_menu_views.flash_sell_products,name='flash_sell_products'),
    path('products/brand/<int:brand_id>/', main_menu_views.brand_wise_products_view, name='brand_wise_products'),
    path('products/campaign/<int:campaign_id>/',main_menu_views.campaign_products_view,name='campaign_products'),
    path('categories/',main_menu_views.categories_list,name='all_categories'),
    path('sub-category/products/<int:sub_cat_id>/', main_menu_views.sub_category_product_show_view, name="sub_category_products_shows_url"),
    path('just-for-you/', main_menu_views.just_for_you_products_show_view, name='just_for_you_products_url'),
    

    # PRODUCTS
    path('products/<int:pk>', main_menu_views.products_page_view, name='products_page_url'),
    path('product-details/<int:pk>', main_menu_views.products_details_page_view, name='product_details_page_url'),
    path('digital-products/', main_menu_views.digital_products_page_view, name='digital_products_page_url'),
    path('product-search/', main_menu_views.product_search_view, name='product_search_url'),


    # ADD AND REMOVE PRODUCT TO CART
    path('add-to-cart/', cart_wishlist_views.add_to_cart_view, name='add_to_cart_url'),
    path('cart/update-quantity/', cart_wishlist_views.update_cart_quantity, name='update_cart_qty_url'),
    path('delete-product/', cart_wishlist_views.delete_product_from_cart, name='delete_product_from_cart_url'),
    
    # ADD AND REMOVE PRODUCT TO WISHLIST
    path('add-to-wishlist/', cart_wishlist_views.add_product_to_wishlist, name='add_to_wishlist_url'),
    path('checkout/', cart_wishlist_views.product_checkout_view, name='product_checkout_url'),
    path('buy-now/<int:attribute_id>/', cart_wishlist_views.buy_now_products_view, name='buy_now_product_url'),

    # USER DASHBOARD
    path('user-dashboard/', user_dashboard_views.user_dashboard_views, name="user_dashboard_url"),
    path('user-profile/', user_dashboard_views.user_profile_view, name='user_profile_view_url'),
    path('user-profile/update', user_dashboard_views.user_profile_update_view, name='user_profile_update_url'),
    path('wishlist/', user_dashboard_views.product_wishlist_view, name='product_wishlist_url'),
    path('orders/list', user_dashboard_views.user_order_list_view, name ='user_order_list_url'),
    path("orders/<str:order_status>/", user_dashboard_views.user_order_list_view, name="user_order_list_by_status"),
    path('user-order-detail/<int:order_id>', user_dashboard_views.user_order_details_view, name= 'user_order_detail_url'),
    path('guest-user-order-detail/<int:order_id>', user_dashboard_views.guest_user_order_details_view, name= 'guest_user_order_detail_url'),
    path("order/<int:order_id>/download/",user_dashboard_views.download_order_details_pdf, name="download_order_details"),
    path('order-invoice/download/<int:order_id>/', user_dashboard_views.download_order_invoice_view, name='order_invoice_download_url'),
    path('user-change-password/', user_dashboard_views.user_change_password_view, name = 'user_change_password_url'),
    
    # CONTACT
    path('contact/', footer_views.contact_page_view, name='contact_page_url'),
    path('terms-condition/', footer_views.client_terms_and_conditions_view, name='client_terms_and_conditino_url'),
    path('privacy-policy/', footer_views.client_privecy_and_policy_view, name='client_privecy_and_policy_url'),
    path('return-refund/', footer_views.client_return_and_refund_view, name='client_return_and_refund_url'),
    path('warranty-policy/', footer_views.client_warranty_policy_view, name='client_warranty_policy_url'),
    path('emi-policy/', footer_views.client_emi_policy_view, name='client_emi_policy_url'),
    path('about-us/', footer_views.client_about_us_view, name='client_about_us_url'), 

    # THEME SETTING
    path('theme-setting/', theme_setting_views.theme_setting_view, name='theme_setting_url'),

    # AJAX
    path('color-size-load/', main_menu_views.get_variant_data, name='get_variant_data'),
    path('ajax/get-subcategories/', filter_views.get_subcategories, name='get_subcategories'),
    path('ajax/get-subsubcategories/', filter_views.get_subsubcategories, name='get_subsubcategories'),
    path('ajax/get-subsub-categories-from-category/', filter_views.get_subsub_categories_from_category, name='get_subsub_categories_from_category'),

    path('ajax/get-brands-from-category/', filter_views.get_brands_from_category, name='get_brands_from_category'),
    path('ajax/get-colors-from-category/', filter_views.get_colors_from_category, name='get_colors_from_category'),
    path('ajax/get-sizes-from-category/', filter_views.get_sizes_from_category, name='get_sizes_from_category'),

    path('ajax/get-brands-from-sub-category/', filter_views.get_brands_from_sub_category, name='get_brands_from_sub_category'),
    path('ajax/get-colors-from-sub-category/', filter_views.get_colors_from_sub_category, name='get_colors_from_sub_category'),
    path('ajax/get-sizes-from-sub-category/', filter_views.get_sizes_from_sub_category, name='get_sizes_from_sub_category'),

    path('ajax/get-brands-from-sub-sub-category/', filter_views.get_brands_from_sub_sub_category, name='get_brands_from_sub_sub_category'),
    path('ajax/get-colors-from-sub-sub-category/', filter_views.get_colors_from_sub_sub_category, name='get_colors_from_sub_sub_category'),
    path('ajax/get-sizes-from-sub-sub-category/', filter_views.get_sizes_from_sub_sub_category, name='get_sizes_from_sub_sub_category'),

    path('ajax/get-sizes-from-brand/', filter_views.get_sizes_from_brand, name='get_sizes_from_brand'),
    path('ajax/get-colors-from-brand/', filter_views.get_colors_from_brand, name='get_colors_from_brand'),

    path('ajax/get-sizes-from-color/', filter_views.get_sizes_from_color, name='get_sizes_from_color'),

    # ajax for brand

    path('ajax/get-subcategories-from-category/', filter_views.get_subcategories_from_category, name='get_subcategories_from_category'),
    path('ajax/get-sub-sub-categories-from-category/', filter_views.get_sub_sub_categories_from_category, name='get_subsub_categories_from_category'),
    path('ajax/get-colors-from-category-for-brand/', filter_views.get_colors_from_category_for_brand, name='get_colors_from_category_for_brand'),
    path('ajax/get-sizes-from-category-for-brand/', filter_views.get_sizes_from_category_for_brand, name='get_sizes_from_category_for_brand'),
    path('ajax/get-brands-from-category-for-brand/', filter_views.get_brands_from_category_for_brand, name='get_brands_from_category_for_brand'),


    path('ajax/get-sub-sub-categories-from-sub-category-for-brand/', filter_views.get_sub_sub_category_from_sub_category_for_brand, name='get_sub_sub_categories_from_sub_category_for_brand'),
    path('ajax/get-colors-from-sub-category-for-brand/', filter_views.get_colors_from_sub_category_for_brand, name='get_colors_from_sub_category_for_brand'),
    path('ajax/get-sizes-from-sub-category-for-brand/', filter_views.get_sizes_from_sub_category_for_brand, name='get_sizes_from_sub_category_for_brand'),

    path('ajax/get-colors-from-sub-sub-category-for-brand/', filter_views.get_colors_from_sub_sub_category_for_brand, name='get_colors_from_sub_sub_category_for_brand'),
    path('ajax/get-sizes-from-sub-sub-category-for-brand/', filter_views.get_sizes_from_sub_sub_category_for_brand, name='get_sizes_from_sub_sub_category_for_brand'),

    path('ajax/get-sizes-from-color-for-brand/', filter_views.get_sizes_from_color_for_brand, name='get_sizes_from_color_for_brand'),


    # REVIEW RATING
    path('submit-review/', main_menu_views.submit_review_view, name='submit_review_url'),



]
