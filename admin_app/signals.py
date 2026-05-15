from django.db.models.signals import post_migrate, post_delete
from django.dispatch import receiver
from admin_app.models import admin_dashboard_models

@receiver(post_migrate)
def create_default_theme(sender, **kwargs):
    if not admin_dashboard_models.ThemeSetting.objects.exists():
        admin_dashboard_models.ThemeSetting.objects.create()

@receiver(post_delete, sender=admin_dashboard_models.FlashSell)
def update_final_price_on_flash_sale_change(sender, instance, **kwargs):
    product = instance.product
    if not product:
        return

    attributes = admin_dashboard_models.ProductAttribute.objects.filter(product=product)
    for attr in attributes:
        admin_dashboard_models.ProductAttribute.objects.filter(pk=attr.pk).update(
            final_price=attr.calculate_final_price()
        )