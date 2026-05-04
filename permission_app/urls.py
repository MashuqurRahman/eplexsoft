from django.urls import path
from . import views

urlpatterns = [
    path('', views.permission_list, name='permission_list'),
    path('create/', views.permission_create, name='permission_create'),
    path('delete/<int:pk>/', views.permission_delete, name='permission_delete'),
]
