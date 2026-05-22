from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', include('admin_app.urls')),
    path('accounts/', include('accounts_app.urls')),
    path('permissions/', include('permission_app.urls')),
    path('', include('client_app.urls')),
    path('report/', include('report_app.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


