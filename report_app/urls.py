from django.urls import path
from .views import reports_views
urlpatterns =[
    path('stock_report/', reports_views.stock_reports_views, name='stock_report_url'),
    path('order-report/', reports_views.order_report_views, name='order_report_url'),
]