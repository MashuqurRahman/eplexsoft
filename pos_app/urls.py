from django.urls import path, include
from pos_app.views import dashboard_views, master_setup_data_views, inventory_views

master_patterns = [
    path('branch/', master_setup_data_views.branch_setup_view, name='branch_setup_url'),
    path('branch-delete/<int:pk>/', master_setup_data_views.branch_delete_view, name='branch_delete_url'),

    # POS USER
    path('user/index/', master_setup_data_views.pos_user_list_view, name='pos_user_list_url'), 
    path('user/create/', master_setup_data_views.pos_user_create_view, name='pos_user_create_url'), 
    path('user/update/<int:pk>/', master_setup_data_views.pos_user_update_view, name='pos_user_update_url'), 
    path('user/delete/<int:pk>/', master_setup_data_views.pos_user_delete_view, name='pos_user_delete_url'), 
]

inventory_patterns = [
    path('supplier/index/', inventory_views.supplier_index_view, name='supplier_index_url'),
    path('supplier/create/', inventory_views.supplier_create_view, name='supplier_create_url'),
    path('supplier/list/', inventory_views.supplier_list_view, name='supplier_list_url'),
    path('supplier/update/<int:pk>/', inventory_views.supplier_update_view, name='supplier_update_url'),
    path('supplier/delete/<int:pk>/', inventory_views.supplier_delete_view, name='supplier_delete_url'),
]


urlpatterns = [
    path('', dashboard_views.pos_dashboard_view, name='pos_dashboard_url'),
    path('master-setup/', include(master_patterns)),
    path('inventory/', include(inventory_patterns)),
]
