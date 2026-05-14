import re
from django import forms
from admin_app.models import admin_dashboard_models
from ..models import client_models

class ContactForm(forms.ModelForm):
    class Meta:
        model = client_models.Contact
        fields = "__all__"
        labels = {
            'full_name': "Full Name",
            'phone_no': "Phone Number",
        }
        widgets = {
            'message': forms.TextInput(attrs={'rows': 1, 'cols': 1})
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.ShippingAddress
        fields = "__all__"
        labels = {
            'full_name': "Full Name",
            'address_line': "Address",
            'postal_code': "Postal Code",
            'phone_no': "Phone No",
            'upozila': "Upazila"
        }
        widgets = {
            'address_line': forms.TextInput(attrs={'rows': 4, 'cols': 4})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone_no')
        if phone:
            phone = phone.strip()
            pattern = r'^(01[3-9]\d{8})$'

        if not re.match(pattern, phone):
            self.add_error('phone_no', "Please enter correct phone number")
        return cleaned_data

    


class TearmsConditionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = admin_dashboard_models.TermsCondition
        fields = "__all__"
        labels = {
            'is_active': "Active"
        }
        widgets = {
            'description': forms.Textarea(attrs={"id": "id_description"}),
            'head': forms.Select(attrs={"class": "form-control select2"})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['head'].required = True

    def clean(self):
        cleaned_data = super().clean()
        head = cleaned_data.get('head')
        if admin_dashboard_models.TermsCondition.objects.filter(head=head).exclude(id=self.instance.id).exists():
            self.add_error('head', "Terms and Condition already exists. Please Update it instead of creating new one.")
        return cleaned_data


class PrivecyPolicyForm(forms.ModelForm):
    description = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = admin_dashboard_models.PrivacyPolicy
        fields = "__all__"
        labels = {
            'is_active': "Active"
        }
        widgets = {
            'description': forms.Textarea(attrs={"id": "id_description"})
        }

class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.ClientThemeSetting
        fields = "__all__"
        label = {
            'footer_color': "Footer Color",
            'notification_color': "Notification Color",
            'price_color': "Price Color",
            'button_color': "Button Color",
        }
        widgets = {
            'footer_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'notification_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'price_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'button_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }

class AboutUsForm(forms.ModelForm):
    description = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = admin_dashboard_models.AboutUs
        fields = "__all__"
        labels = {
            'is_active': "Active"
        }
        widgets = {
            'description': forms.Textarea(attrs={"id": "id_description"})
        }