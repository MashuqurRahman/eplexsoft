from django.db import models

class BrachName(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
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