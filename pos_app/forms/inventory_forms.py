import re
from django import forms
from django.core.exceptions import ValidationError
from pos_app.models import pos_models

class SupplierForm(forms.ModelForm):
    class Meta:
        model = pos_models.Supplier
        fields = "__all__"
        widgets = {
            'address': forms.TextInput(attrs={'rows': 1, 'cols': 1})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "--SELECT--"

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if not email:
            return email
        qs = pos_models.Supplier.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email already exists.")
 
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r'[0-9+\-]+', phone):
            raise forms.ValidationError("Phone number can only contain digits")
 
        qs = pos_models.Supplier.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This phone number already exists.")
 
        return phone