from django.db.models.signals import post_migrate
from django.dispatch import receiver
from admin_app.models import admin_dashboard_models

@receiver(post_migrate)
def create_default_theme(sender, **kwargs):
    if not admin_dashboard_models.ClientThemeSetting.objects.exists():
        admin_dashboard_models.ClientThemeSetting.objects.create()