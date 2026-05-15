from django import forms
from ..models import admin_dashboard_models

class ThemeSettingForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.ThemeSetting
        fields = ['primary_color', 'secondary_color']
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }

class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.SiteSetting
        fields = "__all__"
        excludes = ['company_google_app', 'company_apple_app']
        labels = {
            'company_name': 'Company Name',
            'company_moto': 'Company Moto',
            'contact_phone': 'Contact Phone',
            'facebook': 'Facebook URL',
            'whatsapp_no': 'WhatsApp Number',
            'messenger': 'Messenger URL',
            'youtube': 'YouTube URL',
            'linkedin': 'LinkedIn URL',
            'instagram': 'Instagram URL',
            'tiktok': 'TikTok URL',
            'xhandle': 'X (Twitter) Handle URL'
        }

class PaymentMethodLogoForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.paymentMethodLogos
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        logo = cleaned_data.get('logo')

        if admin_dashboard_models.paymentMethodLogos.objects.filter(logo__icontains=logo).exists():
            self.add_error('logo', "This logo already exists. Please choose a different image.")
        return cleaned_data

        