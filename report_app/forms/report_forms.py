from django import forms
from admin_app.models import admin_dashboard_models
from admin_app.models import choices

class StockReportForm(forms.Form):                                                              #nja

    categories = forms.ModelChoiceField(queryset=admin_dashboard_models.Categories.objects.all(),required=False, widget=forms.Select(attrs={'class': 'select2 form-control'}), label="Category", empty_label="--SELECT--")
    sub_categories = forms.ModelChoiceField(queryset=admin_dashboard_models.SubCategories.objects.all(),required=False, widget=forms.Select(attrs={'class': 'select2 form-control'}), label="Sub Category", empty_label="--SELECT--")
    sub_sub_categories = forms.ModelChoiceField(queryset=admin_dashboard_models.SubSubCategories.objects.all(),required=False, widget=forms.Select(attrs={'class': 'select2 form-control'}), label="Sub Sub Category", empty_label="--SELECT--")
    stock = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter stock threshold'}), label="Stock Less Than or Equal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category_value = self.data.get('categories') or self.initial.get('categories')
        sub_category_value = self.data.get('sub_categories') or self.initial.get('sub_categories')


        if category_value:
            try:
                category_id = int(category_value)
                self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.filter(
                    categories_id=category_id
                )
            except (ValueError, TypeError):
                pass
        else:
            self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.all()


        if sub_category_value:
            try:
                sub_category_id = int(sub_category_value)
                self.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.filter(
                    sub_categories_id=sub_category_id
                )
            except (ValueError, TypeError):
                pass
        else:
            self.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.all()



class OrderReportForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=admin_dashboard_models.Categories.objects.all(),required=False, widget=forms.Select(attrs={'class': 'select2 form-control'}), label="Category", empty_label="--SELECT--")
    sub_categories = forms.ModelChoiceField(queryset=admin_dashboard_models.SubCategories.objects.all(),required=False, widget=forms.Select(attrs={'class': 'select2 form-control'}), label="Sub Category", empty_label="--SELECT--")
    sub_sub_categories = forms.ModelChoiceField(queryset=admin_dashboard_models.SubSubCategories.objects.all(),required=False, widget=forms.Select(attrs={'class': 'select2 form-control'}), label="Sub Sub Category", empty_label="--SELECT--")
    order_status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select2 form-control'}),choices=choices.ORDER_STATUS_CHOICES, required=False, label="Order Status")
    form_date = forms.DateField(label="Form Date", widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label="To Date", widget=forms.DateInput(attrs={'type': 'date'}))


    def clean(self):
        cleaned_data = super().clean()
        form_date = cleaned_data.get('form_date')
        to_date = cleaned_data.get('to_date')

        if form_date and to_date:
            if form_date > to_date:
                self.add_error("form_date", "Form date cannot be greater than To date.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'categories' in self.data:
            try:
                category_id = int(self.data.get('categories'))
                self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.filter(categories_id=category_id)
            except (ValueError, TypeError):
                pass

        if 'sub_categories' in self.data:
            try:
                sub_category_id = int(self.data.get('sub_categories'))
                self.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories_id=sub_category_id)
            except (ValueError, TypeError):
                pass
