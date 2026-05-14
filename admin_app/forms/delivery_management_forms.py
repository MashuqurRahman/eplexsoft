from django import forms
from datetime import date
from ..models import admin_dashboard_models

class DeliveryChargeForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.DeliveryCharge
        fields = ['initial_charge', 'initial_weight', 'increment_weight_per_unit','delivery_location', 'is_active']
        labels = {
            'sub_sub_category': "Sub Sub Category",
            'initial_charge': "Initial Charge",
            'initial_weight': "Initial Weight",
            'initial_unit': "Base Unit",
            'increment_weight_per_unit': "Increment Per Excess KG",
            'unit': "Increment Unit",
            'delivery_location': "Location",
            'is_active': "Active"
        }
        widgets = {
            'unit': forms.Select(attrs={'class': "select2 form-control"}),
            'initial_unit': forms.Select(attrs={'class': "select2 form-control"}),
            'delivery_location': forms.Select(attrs={'class': "select2 form-control"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['initial_charge'].required = True
        self.fields['initial_weight'].required = True
        self.fields['increment_weight_per_unit'].required = True


class DeliveryDiscountForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.DeliveryDiscount
        fields = "__all__"
        labels = {
            'flat_delivery': "Flat Delivery",
            'discount_price': "Discount Price",
            'min_price': "Minimum Price"
        }
        widgets = {
            'type': forms.Select(attrs={'class': "select2 form-control"}),
        }


class CouponManagementForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.CouponManagement
        fields = "__all__"
        labels = {
            'is_percent': "Is Percent",
            'start_date': "Start Date",
            'end_date': "End Date",
            'min_price': "Minimum Price",
            'number_of_user': "Number of Use",
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'type': forms.Select(attrs={'class': "select2"})
        }

    def clean(self):
        cleaned_data =  super().clean()
        code = cleaned_data.get('code')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        value = cleaned_data.get('value')
        is_percent = cleaned_data.get('is_percent')
        
        if admin_dashboard_models.CouponManagement.objects.filter(code=code).exists():
            self.add_error('code', "Coupon code already exists")

        if start_date is not None and start_date < date.today():
            self.add_error('start_date', "Start date cannot be in the past")
            
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                self.add_error('start_date', "Start Date must be before End Date")

        if value is not None:
            if value > 100 and is_percent == True:
                self.add_error('value', "Value must be less than or equal to 100")

        return cleaned_data
    

class CouponManagementUpdateForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.CouponManagement
        fields = "__all__"
        labels = {
            'is_percent': "Is Percent",
            'start_date': "Start Date",
            'end_date': "End Date",
            'min_price': "Minimum Price",
            'number_of_user': "Number of Use",
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'type': forms.Select(attrs={'class': "select2"})
        }

    def clean(self):
        cleaned_data =  super().clean()
        code = cleaned_data.get('code')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        value = cleaned_data.get('value')
        is_percent = cleaned_data.get('is_percent')
        
        if start_date is not None and start_date < date.today():
            self.add_error('start_date', "Start date cannot be in the past")
            
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                self.add_error('start_date', "Start Date must be before End Date")

        if value is not None:
            if value > 100 and is_percent == True:
                self.add_error('value', "Value must be less than or equal to 100")

        return cleaned_data