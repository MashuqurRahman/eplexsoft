from django.urls import path

from accounts_app import views
from courier import views as courier_views
from .views import dashboard_views, categories_views, products_views, products_management_views, footer_views,order_views,site_setting_views,ajax_views,slider_views, promotion_management_views, delivery_management_views, coupon_management_views, employee_management, theme_setting_views, review_management_views, courier_views as admin_courier_views
from .recommendation import similarity

urlpatterns = [
    path('', dashboard_views.admin_dashboard_view, name='admin_dashboard_url'),

    # CATEGORIES URLS
    path('categories-list/', categories_views.categories_index_view, name='categories_list_url'),
    path('add-categories/', categories_views.add_categories_view, name='add_categories_url'),
    path('edit-categories/<int:pk>/', categories_views.update_categories_view, name='edit_categories_url'),
    path('delete-categories/<int:pk>/', categories_views.delete_categories_view, name='delete_categories_url'),
    path('search-categories/', categories_views.search_categories_view, name='search_categories_url'),

    # SUB CATEGORIES URLS
    path('sub-categories-list/', categories_views.sub_categories_index_view, name='sub_categories_index_url'),
    path('add-sub-categories/', categories_views.add_sub_categories_view, name='add_sub_categories_url'),
    path('edit-sub-categories/<int:pk>/', categories_views.update_sub_categories_view, name='update_sub_categories_url'),
    path('delete-sub-categories/<int:pk>/', categories_views.delete_sub_categories_view, name='delete_sub_categories_url'),
    path('search-sub-categories/', categories_views.search_sub_categories_view, name='search_sub_categories_url'),

    # SUB SUB CATEGORIES URLS
    path('sub-sub-categories-list/', categories_views.sub_sub_categories_index_view, name='sub_sub_cat_index_url'),
    path('add-sub-sub-categories/', categories_views.add_sub_sub_categories_view, name='add_sub_sub_categories_url'),
    path('edit-sub-sub-categories/<int:pk>/', categories_views.update_sub_sub_categories_view, name='update_sub_sub_categories_url'),
    path('delete-sub-sub-categories/<int:pk>/', categories_views.delete_sub_sub_categories_view, name='delete_sub_sub_categories_url'),
    path('search/sub-sub-categories/', categories_views.search_sub_sub_categories_view, name='search_sub_sub_categories_url'),

    # PRODUCTS URLS
    path('products-list/', products_views.product_list_index_view, name='products_list_url'),
    path('add-products/', products_views.add_product_view, name='add_product_url'),
    path('products-details/<int:pk>/', products_views.product_details_view, name='product_details_url'),
    path('update-products/<int:pk>/', products_views.update_product_view, name='update_product_url'),
    path('delete-products/<int:pk>/', products_views.delete_product_view, name='delete_product_url'),
    path('search-products/', products_views.search_products_view, name='search_product_url'),

    # PRODUCTS ATTRIBUTES
    path('product-attribute/create/<int:pk>/', products_views.product_attribute_create_view, name='product_attribute_create_url'),
    path('product-attribute/update/<int:pk>/', products_views.product_attribute_update_view, name='product_attribute_update_url'),
    path('product-attribute/delete/<int:pk>/<int:product_id>/', products_views.product_attribute_delete_view, name='product_attribute_delete_url'),
    path('delete-attribute-image/<int:pk>/', products_views.delete_attribute_image, name='delete_attribute_image'),

    # BRAND URLS
    path('brand-list/', products_management_views.brand_list_view, name='brand_list_url'),
    path('add-brand/', products_management_views.add_brand_view, name='add_brand_url'),
    path('update-brand/<int:pk>/', products_management_views.update_brand_view, name='update_brand_url'),
    path('delete-brand/<int:pk>/', products_management_views.delete_brand_view, name='delete_brand_url'),
    path('search-brand/', products_management_views.search_brand_view, name='search_brand_url'),

    # COLOR URLS
    path('color-list/', products_management_views.color_list_view, name='color_list_url'),
    path('add-color/', products_management_views.add_color_view, name='add_color_url'),
    path('update-color/<int:pk>/', products_management_views.update_color_view, name='update_color_url'),
    path('delete-color/<int:pk>/', products_management_views.delete_color_view, name='delete_color_url'),
    path('search-color/', products_management_views.search_color_view, name='search_color_url'),

    # SIZE URLS
    path('size-list/', products_management_views.size_list_view, name='size_list_url'),
    path('add-size/', products_management_views.add_size_view, name='add_size_url'),
    path('update-size/<int:pk>/', products_management_views.update_size_view, name='update_size_url'),
    path('delete-size/<int:pk>/', products_management_views.delete_size_view, name='delete_size_url'),
    path('search-size/', products_management_views.search_size_view, name='search_size_url'),

    # UNIT URLS
    path('unit-list/', products_management_views.unit_list_view, name='unit_list_url'),
    path('add-unit/', products_management_views.add_unit_view, name='add_unit_url'),
    path('update-unit/<int:pk>/', products_management_views.update_unit_view, name='update_unit_url'),
    path('delete-unit/<int:pk>/', products_management_views.delete_unit_view, name='delete_unit_url'),

    # CONTACT URLS
    path('contact/', footer_views.admin_contact_view, name='admin_contact_url'),
    
    #order URLS
    # path("orders/<str:order_status>/", order_views.order_list, name="order_list"),
    path("orders/", order_views.order_list, name="order_list"),
    path('orders/product-variants/', order_views.get_product_variants_ajax, name='get_product_variants_ajax'),
    path('orders/update-order/', order_views.update_order_ajax, name='update_order_ajax'),
    path('orders/search-products/', order_views.search_products_ajax, name='search_products_ajax'),
    path('orders/update-shipping-address/', order_views.update_shipping_address_ajax, name='update_shipping_address_ajax'),
    path('orders/update-shipping-method/', order_views.update_shipping_method_ajax, name='update_shipping_method_ajax'),
    path('orders/<int:order_id>/edit/', order_views.order_edit_view, name='order_edit_url'),
    path("orders/<str:order_status>/", order_views.order_list, name="order_list_by_status"),
    path('orders-detail/<int:order_id>/', order_views.order_detail_view, name='order_detail'),
    path('update-order-status/', order_views.update_order_status, name='update_order_status'),
    path('update-payment-status/', order_views.update_payment_status, name='update_payment_status'),
    path('ordered-product/search/', order_views.search_ordered_product, name='search_ordered_product'),

    # ALL PRODUCTS URLS
    # path('all-products/', products_views.all_product_list_view, name='all_products_url'),
    # path('product-add/', products_views.product_add_view, name='product_add_url'),
    # path('product-update/<int:pk>/', products_views.product_update_view, name='product_update_url'),
    # path('product-delete/<int:pk>/', products_views.product_delete_view, name='product_delete_url'),
    # path('products-details/<int:pk>/', products_views.product_details_view, name='product_details_url'),
    # site_setting
    path('site-settings/', site_setting_views.site_setting_list, name='site_setting_list'),
    path('site-settings/create/', site_setting_views.site_setting_create, name='site_setting_create'),
    path('site-settings/update/<int:pk>/', site_setting_views.site_setting_update, name='site_setting_update'),
    path('site-settings/delete/<int:pk>/', site_setting_views.site_setting_delete, name='site_setting_delete'),

    # payment method logos
    path('payment-method-logos/', site_setting_views.payment_method_logs_list, name='payment_method_logo_list'),
    path('payment-method-logos/create/', site_setting_views.payment_method_logo_create, name='payment_method_logo_create'),
    path('payment-method-logos/update/<int:pk>/', site_setting_views.payment_method_logo_update, name='payment_method_logo_update'),
    path('payment-method-logos/delete/<int:pk>/', site_setting_views.payment_method_logo_delete, name='payment_method_logo_delete'),

    # AJAX
    path('ajax/load-subcategories/', ajax_views.load_sub_category, name='ajax_load_subcategories'),
    path('ajax/load-sub-subcategories/', ajax_views.load_sub_sub_category, name='ajax_load_sub_subcategories'),
    path('ajax/load-sub-subcategories_form_category/', ajax_views.load_sub_sub_category_from_category, name='ajax_load_sub_subcategories_from_category'),
    path('ajax/load-products', ajax_views.ajax_load_products, name='ajax_load_products'),
    # path('ajax/calculate-delivery/', ajax_views.calculate_delivery_ajax, name='calculate_delivery'),
    path("apply-coupon/", ajax_views.apply_coupon, name="apply_coupon"),
    path("ajax/load-product-table/", ajax_views.ajax_load_product_table, name='ajax_load_product_table'),
    path("ajax/update-quantity/", ajax_views.ajax_update_cart_quantity, name='ajax_update_cart_quantity'),




    path('side-sliders/', slider_views.side_slider_list, name='campaign_list'),
    path('side-sliders/create/', slider_views.side_slider_create, name='campaign_create'),
    path('side-sliders/<int:pk>/edit/', slider_views.side_slider_update, name='campaign_update'),
    path('side-sliders/<int:pk>/delete/', slider_views.side_slider_delete, name='campaign_delete'),


    path('sliders/', slider_views.slider_list, name='slider_list'),
    path('sliders/create/', slider_views.slider_create, name='slider_create'),
    path('sliders/<int:pk>/edit/', slider_views.slider_update, name='slider_update'),
    path('sliders/<int:pk>/delete/', slider_views.slider_delete, name='slider_delete'),

    # FLASH SELL
    path('flash-sale/index/', promotion_management_views.product_flash_sell_index_view, name='flash_sell_index_url'),
    path('flash-sale/create/', promotion_management_views.product_flash_sell_create_view, name='flash_sell_create_url'),
    path('flash-sale/update/<int:pk>/', promotion_management_views.product_flash_sell_update_view, name='flash_sell_update_url'),
    path('flash-sale/delete/<int:pk>/', promotion_management_views.product_flash_sell_delete_view, name='flash_sell_delete_url'),
    path('flash-sale/search/', promotion_management_views.flash_sale_search_view, name='flash_sale_search_url'),

    # DELIVERY CHARGE
    path('delivery-charge/index/', delivery_management_views.delivery_charge_index_view, name='delivery_charge_index_url'),
    path('delivery-charge/create/', delivery_management_views.delivery_charge_create_view, name='delivery_charge_create_url'),
    path('delivery-charge/update/<int:pk>/', delivery_management_views.delivery_charge_update_view, name='delivery_charge_update_url'),
    path('delivery-charge/delete/<int:pk>/', delivery_management_views.delivery_charge_delete_view, name='delivery_charge_delete_url'),

    # DELIVERY DISCOUNT
    path('delivery-discount/index/', delivery_management_views.delivery_discount_index_view, name='delivery_discount_index_url'),
    path('delivery-discount/create/', delivery_management_views.delivery_discount_create_view, name='delivery_discount_create_url'),
    path('delivery-discount/update/<int:pk>/', delivery_management_views.delivery_discount_update_view, name='delivery_discount_update_url'),
    path('delivery-discount/delete/<int:pk>/', delivery_management_views.delivery_discount_delete_view, name='delivery_discount_delete_url'),

    # COUPON MANAGEMENT
    path('coupon/index/', coupon_management_views.coupon_management_index_view, name='coupon_index_url'),
    path('coupon/create/', coupon_management_views.coupon_management_create_view, name='coupon_create_url'),
    path('coupon/update/<int:pk>/', coupon_management_views.coupon_management_update_view, name='coupon_update_url'),
    path('coupon/delete/<int:pk>/', coupon_management_views.coupon_management_delete_view, name='coupon_delete_url'),
    path('coupon/search/', coupon_management_views.search_coupon_view, name='coupon_search_url'),

    # Update Recommendation
    path('update/just-for-you/', similarity.build_similarity_matrix, name='update_just_for_you'),

    # USER MANAGEMENT
    path('employee-list/', employee_management.all_employee_view, name='all_employee_url'),
    path('add-employee/', employee_management.add_employee_view, name='add_employee_url'),
    path('update-employee/information/<int:pk>/', employee_management.update_employee_details_view, name='update_employee_url'),
    path('eployee-profile/<int:pk>/', employee_management.empolyee_profile_view, name='employee_profile_url'),
    path('delete-employee/<int:pk>/', employee_management.delete_employee_view, name='delete_employee_url'),
    path('search-employee/', employee_management.search_empolyee_view, name='search_employee_url'),

    # TERMS & CONDITIONS
    path('terms-condition/index/', footer_views.terms_and_condition_index_view, name='terms_and_conditions_index_url'),
    path('terms-condition/create/', footer_views.terms_and_conditions_create_view, name='terms_and_conditions_create_url'),
    path('terms-condition/update/<int:pk>/', footer_views.terms_and_conditions_update_view, name='terms_and_conditions_update_url'),
    path('terms-condition/delete/<int:pk>/', footer_views.terms_and_conditions_delete_view, name='terms_and_conditions_delete_url'),

    # PRIVECY & POLICY
    path('privecy-policy/index/', footer_views.privecy_and_policy_index_view, name='privecy_and_policy_index_url'),
    path('privecy-policy/create/', footer_views.privecy_and_policy_create_view, name='privecy_and_policy_create_url'),
    path('privecy-policy/update/<int:pk>/', footer_views.privecy_and_policy_update_view, name='privecy_and_policy_update_url'),
    path('privecy-policy/delete/<int:pk>/', footer_views.privecy_and_policy_delete_view, name='privecy_and_policy_delete_url'),

    # ABOUT US
    path('about-us/index/', footer_views.about_us_index_view, name='about_us_index_url'),
    path('about-us/create/', footer_views.about_us_create_view, name='about_us_create_url'),
    path('about-us/update/<int:pk>/', footer_views.about_us_update_view, name='about_us_update_url'),
    path('about-us/delete/<int:pk>/', footer_views.about_us_delete_view, name='about_us_delete_url'),

    # THEME SETTINGS
    path('theme-settings/', theme_setting_views.theme_setting_view, name='theme_settings'),

    # REVIEW MANAGEMENT
    path('reviews/', review_management_views.review_list_view, name='review_list_url'),
    path('reviews/delete/<int:review_id>/', review_management_views.delete_review_view, name='delete_review_url'),
    path('reviews/update/<int:review_id>/', review_management_views.review_update_view, name='update_review_url'),
    path('reviews/toggle-selection/', review_management_views.toggle_review_selection, name='toggle_review_selection_url'),
    path('reviews/search/', review_management_views.review_search_view, name='review_search_url'),


    # STEADFAST URLS
    path('order/<int:order_id>/send-courier/', courier_views.send_to_steadfast_view, name='send_to_steadfast'),
    path('order/<int:order_id>/track-courier/', courier_views.track_order_view, name='track_order'),
    path('courier/balance/', courier_views.courier_balance_view, name='courier_balance'),
    path('webhook/steadfast/', courier_views.steadfast_webhook, name='steadfast_webhook'),

    # COURIER
    path('courier/index/', admin_courier_views.courier_index_view, name="courier_index_url"),
    path('courier/create/', admin_courier_views.courier_create_view, name="courier_create_url"),
    path('courier/update/<int:pk>/', admin_courier_views.courier_update_view, name="courier_update_url"),
    path('pathao_courier/update/<int:pk>/', admin_courier_views.pathao_courier_update_view, name="pathao_courier_update_url"),
    path('redx_courier/update/<int:pk>/', admin_courier_views.redx_courier_update_view, name="redx_courier_update_url"),
    path('courier/delete/<int:pk>/', admin_courier_views.courier_delete_view, name="courier_delete_url"),
    path('pathao_courier/delete/<int:pk>/', admin_courier_views.pathao_courier_delete_view, name="pathao_courier_delete_url"),
    path('redx_courier/delete/<int:pk>/', admin_courier_views.redx_courier_delete_view, name="redx_courier_delete_url"),

    path('bulk-courier-form/', admin_courier_views.bulk_courier_form, name='bulk_courier_form'),
    path('refresh-consignment/<int:order_id>/', admin_courier_views.refresh_consignment_status_view, name='refresh_consignment'),
]

