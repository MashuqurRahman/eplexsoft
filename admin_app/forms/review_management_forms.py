from django import forms
from client_app.models import client_models

class ReviewRatingForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = client_models.ReviewRating
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 1, 'cols': 40})
        }
    