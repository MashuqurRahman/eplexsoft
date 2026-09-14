from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from pos_app.models import choices

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

class PosProduct(models.Model):
    attribute = models.ForeignKey('admin_app.ProductAttribute', on_delete=models.PROTECT, related_name='pos_product_attribute')
    branch = models.ForeignKey(BrachName, on_delete=models.PROTECT, related_name='pos_product_branch')
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.branch.name}/{self.attribute.product.product_name}'

class StockPullRequest(models.Model):
    attribute = models.ForeignKey('admin_app.ProductAttribute', on_delete=models.PROTECT, related_name='stock_pull_requests')
    requesting_branch = models.ForeignKey(BrachName, on_delete=models.PROTECT, related_name='pull_requests_created')
    source_branch = models.ForeignKey(BrachName, on_delete=models.PROTECT, related_name='pull_requests_received')
    requested_qty = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=choices.STATUS_CHOICES, default='pending')
    request_by = models.ForeignKey('accounts_app.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='pull_requests_made')
    reviewed_by = models.ForeignKey('accounts_app.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='pull_requests_reviewed')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.requesting_branch} <- {self.source_branch} | {self.attribute} x{self.requested_qty} [{self.status}]'

    def clean(self):
        if self.requesting_branch_id and self.source_branch_id and self.requesting_branch_id == self.source_branch_id:
            raise ValidationError('Requesting branch and source branch must be different.')


class StockTransferLog(models.Model):
    pull_request = models.ForeignKey(StockPullRequest, on_delete=models.CASCADE, related_name='logs')
    event = models.CharField(max_length=10, choices=choices.EVENT_CHOICES)
    attribute = models.ForeignKey('admin_app.ProductAttribute', on_delete=models.PROTECT, related_name='stock_transfer_logs')
    requesting_branch = models.ForeignKey(BrachName, on_delete=models.PROTECT, related_name='stock_logs_as_requester')
    source_branch = models.ForeignKey(BrachName, on_delete=models.PROTECT, related_name='stock_logs_as_source')
    qty = models.PositiveIntegerField()
    source_stock_after = models.IntegerField(null=True, blank=True)
    dest_stock_after = models.IntegerField(null=True, blank=True)
    acted_by = models.ForeignKey('accounts_app.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.event}] {self.requesting_branch} <- {self.source_branch} | {self.attribute} x{self.qty}'  