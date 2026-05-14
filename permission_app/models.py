from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from accounts_app.models import User


PRODUCT_APPROVAL_CHOICES = (
    ('', "--SELECT--"),
    ('product_approval_permission', "Product Approval Permission"),
    ('order_management_permission', "Order Management Permission"),
    ('campaign_management_permission', "Campaign Management Permission"),
    ('slider_management_permission', 'Slider  Image Manage Permission'),
    ('employee_management_permission', 'Employee Management Permission'),
    ('permission_management', 'Permission Management'),
    ('category_management', 'Category Manage Permission'),
    ('product_management', 'Product Management Permission'),
    ('product_variant_management', 'Product Variant Management Permission'),
    ('promotion_management', 'Promotion Management Permission'),
    ('delivery_management', 'Delivery Management Permission'),
    ('coupon_management', 'Coupon Management Permission'),
    ('company_info_permission', 'Company Info Manage Permission'),
    ('term_and_condition_permission', 'Term and Condition Manage Permission'),
    ('privacy_policy_permission', 'Privacy Policy Manage Permission'),
    ('update_just_for_you_permission', 'Update Just For You Manage Permission'),
    ('theme_change_permission', 'Theme Change Permission'),
    ('report_permission', 'Report Permission'),
)


class AdminPanelPermissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_panel_permission_user")
    permission= models.CharField(max_length=150, choices=PRODUCT_APPROVAL_CHOICES)

    class Meta:
        unique_together = ('user', 'permission')

    def __str__(self):
        return f"{self.user.email} - {self.permission}"
