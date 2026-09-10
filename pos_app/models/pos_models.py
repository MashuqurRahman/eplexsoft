from django.db import models
# from admin_app.models import admin_dashboard_models

class BrachName(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    payable_amount = models.FloatField(blank=True, null=True)
    due_amount = models.FloatField(blank=True, null=True)
    branch = models.ForeignKey(BrachName, on_delete=models.CASCADE, related_name='supplier_branch_name', blank=True, null=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(BrachName, on_delete=models.CASCADE, related_name='customer_branch_name', blank=True, null=True)

    def __str__(self):
        return self.name

# class PosProduct(models.Model):
#     attribute = models.ForeignKey(admin_dashboard_models.ProductAttribute, on_delete=models.PROTECT, related_name='pos_product_attribute')
#     branch = models.ForeignKey(BrachName, on_delete=models.PROTECT, related_name='pos_product_branch')
#     stock = models.PositiveIntegerField()

#     def __str__(self):
#         return f'{self.branch.name}/{self.attribute.product.product_name}'
        