from django.db import models
from accounts_app.models import User
from admin_app.models import admin_dashboard_models

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.full_name
    
class ReviewRating(models.Model):
    product = models.ForeignKey(admin_dashboard_models.Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveIntegerField(default=1)
    review = models.TextField(blank=True, null=True)
    is_selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.product_name} - {self.rating} Stars"