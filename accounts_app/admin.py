from django.contrib import admin
from admin_app.models import admin_dashboard_models
# Register your models here.
@admin.register(admin_dashboard_models.SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'is_active')