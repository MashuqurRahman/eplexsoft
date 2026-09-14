from django.urls import path, include
from pos_app.views import dashboard_views, master_setup_data_views, inventory_views, ajax_views
from permission_app.views import pos_user_permission_view, save_pos_permission

master_patterns = [
    path('branch/', master_setup_data_views.branch_setup_view, name='branch_setup_url'),
    path('branch-delete/<int:pk>/', master_setup_data_views.branch_delete_view, name='branch_delete_url'),

    # POS USER
    path('user/index/', master_setup_data_views.pos_user_list_view, name='pos_user_list_url'), 
    path('user/create/', master_setup_data_views.pos_user_create_view, name='pos_user_create_url'), 
    path('user/update/<int:pk>/', master_setup_data_views.pos_user_update_view, name='pos_user_update_url'), 
    path('user/delete/<int:pk>/', master_setup_data_views.pos_user_delete_view, name='pos_user_delete_url'), 
    path('user/search/', master_setup_data_views.pos_user_search_view, name='pos_user_search_url'),

    # PERMISSION MANAGEMENT
    path('permission/', pos_user_permission_view, name='pos_user_permission_url'),
    path("permission/save/<int:user_id>/", save_pos_permission, name="save_pos_permission_url"),

    # POS CUSTOMER
    path('customer/index/', master_setup_data_views.pos_customer_index_view, name='pos_customer_index_url'),
    path('customer/create/', master_setup_data_views.pos_customer_create_view, name='pos_customer_create_url'),
    path('customer/update/<int:pk>/', master_setup_data_views.pos_customer_update_view, name='pos_customer_update_url'),
    path('customer/delete/<int:pk>/', master_setup_data_views.pos_customer_delete_view, name='pos_customer_delete_url'),
    path('customer/search/', master_setup_data_views.pos_customer_search_view, name='pos_customer_search_url'),

    # POS PRODUCT
    path('product/index/', master_setup_data_views.pos_product_list_view, name='pos_product_list_url'),
    path('product/create/', master_setup_data_views.pos_product_create_view, name='pos_product_create_url'),
    path('product/update/<int:pk>/', master_setup_data_views.pos_product_update_view, name='pos_product_update_url'),
    path('product/deleted/<int:pk>/', master_setup_data_views.pos_product_delete_view, name='pos_product_delete_url'),
    path('product/search/', master_setup_data_views.pos_product_search_view, name='pos_product_search_url'),
    path('product/subcategories/', master_setup_data_views.pos_get_subcategories_view, name='pos_get_subcategories_url'),

    path('stock-pull/history/', master_setup_data_views.pos_stock_transfer_history, name='stock_transfer_history_url'),
    path('stock-pull/create/', master_setup_data_views.pos_create_pull_request, name='create_pull_request_url'),
    path('stock-pull/sent/', master_setup_data_views.pos_pull_request_list, name='pull_request_list_url'),
    path('stock-pull/received/', master_setup_data_views.pos_received_pull_requests, name='received_pull_requests_url'),
    path('stock-pull/<int:pk>/approve/', master_setup_data_views.pos_approve_pull_request, name='approve_pull_request_url'),
    path('stock-pull/<int:pk>/reject/', master_setup_data_views.pos_reject_pull_request, name='reject_pull_request_url'),

]

inventory_patterns = [
    path('supplier/index/', inventory_views.supplier_index_view, name='supplier_index_url'),
    path('supplier/create/', inventory_views.supplier_create_view, name='supplier_create_url'),
    path('supplier/list/', inventory_views.supplier_list_view, name='supplier_list_url'),
    path('supplier/update/<int:pk>/', inventory_views.supplier_update_view, name='supplier_update_url'),
    path('supplier/delete/<int:pk>/', inventory_views.supplier_delete_view, name='supplier_delete_url'),
    path('supplier/search/', inventory_views.pos_supplier_search_view, name='pos_supplier_search_url'),

    # SUPPLILER DUE
    path('supplier/due/index/', inventory_views.supplier_due_index_view, name='supplier_due_index_url'),
]


urlpatterns = [
    path('', dashboard_views.pos_dashboard_view, name='pos_dashboard_url'),
    path('master-setup/', include(master_patterns)),
    path('inventory/', include(inventory_patterns)),
]
