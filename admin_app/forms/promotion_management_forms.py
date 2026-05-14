from django import forms
from datetime import date
from ..models import admin_dashboard_models

class FlashSellForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=admin_dashboard_models.Categories.objects.all(),
        widget=forms.Select(attrs={'class': 'select2 form-control'}),
        empty_label="--SELECT--"
    )
    
    
    class Meta:
        model = admin_dashboard_models.FlashSell
        fields = "__all__"
        labels = {
            'discount_amount': "Discount Amount",
            'is_percentage': "Is Percentage",
            'start_date': "Start Date",
            'end_date': "End Date",
            'side_slider': "Campaign Type"
        }
        widgets = {
            'side_slider': forms.Select(attrs={'class': 'select2 form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_percentage = cleaned_data.get('is_percentage')
        discount_amount = cleaned_data.get('discount_amount')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date is not None and start_date.date() < date.today():
            self.add_error('start_date', "Start date cannot be in the past")

        if discount_amount is not None:
            if discount_amount > 100 and is_percentage == True:
                self.add_error('discount_amount', "Please enter the value less than or equal to 100%")

        if start_date is not None and end_date is not None:
            if start_date > end_date:
                self.add_error("start_date", "Start Date must be before End Date")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['side_slider'].empty_label = "--SELECT--"
        



class FlashSellUpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=admin_dashboard_models.Categories.objects.all(),
        widget=forms.Select(attrs={'class': 'select2 form-control'}),
        empty_label="--SELECT--"
    )
    sub_category = forms.ModelChoiceField(
        queryset=admin_dashboard_models.SubCategories.objects.all(),
        widget=forms.Select(attrs={'class': 'select2 form-control'}), 
        label="Sub Category", 
        empty_label="--SELECT--"
    )
    sub_sub_category = forms.ModelChoiceField(
        queryset=admin_dashboard_models.SubSubCategories.objects.all(),
        widget=forms.Select(attrs={'class': 'select2 form-control'}),
        label='Sub Sub Category',
        empty_label="--SELECT--"
    )
    
    class Meta:
        model = admin_dashboard_models.FlashSell
        fields = "__all__"
        labels = {
            # 'side_slider': "Side Slilder",
            'discount_amount': "Discount Amount",
            'is_percentage': "Is Percentage",
            'start_date': "Start Date",
            'end_date': "End Date",
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'select2 form-control'}),
            # 'side_slider': forms.Select(attrs={'class': 'select2 form-control'}),
            # 'slider': forms.Select(attrs={'class': 'select2 form-control'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = "--SELECT--"
        self.fields['product'].required = True
        # self.fields['side_slider'].empty_label = "--SELECT--"
        # self.fields['slider'].empty_label = "--SELECT--"