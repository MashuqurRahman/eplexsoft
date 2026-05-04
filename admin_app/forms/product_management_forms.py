from django import forms
from ..models import admin_dashboard_models

class BrandForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Brand
        fields = "__all__"

class ColorForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Color
        fields = "__all__"

class SizeForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Size
        fields = "__all__"

class UnitForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Unit
        fields = "__all__"

