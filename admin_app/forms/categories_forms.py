from django import forms
from ..models import  admin_dashboard_models

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Categories
        fields = "__all__"
        widgets = {
            'description': forms.TextInput(attrs=({'rows': 1, 'cols': 1}))
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if name:
            qs = admin_dashboard_models.Categories.objects.filter(name__iexact=name)

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error('name', "This category name already exists")

        return cleaned_data

        
class SubCategoriesForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.SubCategories
        fields = "__all__"
        widgets = {
            'categories': forms.Select(attrs={'class': 'select2 form-control'}),
            'column': forms.Select(attrs={'class': 'select2 form-control'}),
            'description': forms.TextInput(attrs=({'rows': 1, 'cols': 1}))
        }
        labels = {
            'sub_cat_name': "Sub Category Name",
            'has_sub_sub_cat': "Has Sub Sub Category"
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['categories'].empty_label = "--SELECT--"
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=user, employee__role=role).values_list('category', flat=True)
        if role == 'section_admin' or role == 'employee':
            self.fields['categories'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))



    def clean(self):
        cleaned_data = super().clean()
        cat_name = cleaned_data.get('name')
        categories = cleaned_data.get('categories')
        sub_cat_name = cleaned_data.get('sub_cat_name')
        column = cleaned_data.get('column')
        position = cleaned_data.get('position')

        if admin_dashboard_models.Categories.objects.filter(name__iexact=cat_name).exists():
            self.add_error('name', "This sub category name already exists")

        if categories and sub_cat_name and column and position:
            qs = admin_dashboard_models.SubCategories.objects.filter(
                categories=categories,
                # sub_cat_name__iexact=sub_cat_name,
                column=column,
                position=position
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error('position', "Duplicate: same category, sub category, column and position already exists.")

        return cleaned_data

class SubSubCategoriesForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=admin_dashboard_models.Categories.objects.all(), empty_label='--SELECT--')
    class Meta:
        model = admin_dashboard_models.SubSubCategories
        fields = "__all__"
        widgets = {
            'sub_categories': forms.Select(attrs={'class': 'select2 form-control'}),
        }
        labels = {
            'sub_categories': "Sub Categories",
            'sub_sub_cat_name': "Sub Sub Category Name"
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['sub_categories'].empty_label = "--SELECT--"
        self.fields['categories'].widget.attrs.update({'class': "select2"})
        self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.none()

        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=user, employee__role=role).values_list('category', flat=True)
        if role == 'section_admin' or role == 'employee':
            self.fields['categories'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))

        if 'categories' in self.data :
            try:
                categories_id = int(self.data.get('categories'))
                self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.filter(categories__id=categories_id).order_by('-id')

            
            except (ValueError, TypeError):
                pass
        
        elif self.instance.pk:
            self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        sub_sub_cat_name = cleaned_data.get('name')
        if admin_dashboard_models.Categories.objects.filter(name__iexact=sub_sub_cat_name).exists():
            self.add_error('name', "This sub sub category name already exists")
        return cleaned_data