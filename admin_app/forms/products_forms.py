from django import forms
from ..models import admin_dashboard_models


class ProductForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Product
        fields = "__all__"
        labels = {
            'product_name': "Product Name",
            'categories': "Category",
            'sub_categories': "Sub Category",
            'sub_sub_categories': "Sub Sub Category",
            'moq': "MOQ",
            'is_popular': "Is Popular",
            'is_active': "Active",
            'is_best_deal': "Is Best Deal",
            'is_applicable': "Is VAT/GST Percentage",
            'vat_tax_amount': "VAT Amount",
            'gst_amount': "GST Amount",
            'delivery_discount': "Delivery Discount"
        }
        widgets = {
            'description': forms.TextInput(attrs=({'rows': 1, 'cols': 1})),
            'categories': forms.Select(attrs={'class': 'select2 form-control'}),
            'sub_categories': forms.Select(attrs={'class': 'select2 form-control'}),
            'delivery_discount': forms.Select(attrs={'class': 'select2 form-control'}),
            'sub_sub_categories': forms.Select(attrs={'class': 'select2 form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['categories'].empty_label = '--SELECT--'
        self.fields['sub_categories'].empty_label = '--SELECT--'
        self.fields['delivery_discount'].empty_label = '--SELECT--'
        self.fields['sub_sub_categories'].empty_label = '--SELECT--'
        self.fields['description'].required = True

        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=user, employee__role=role).values_list('category', flat=True)
        if role == 'section_admin' or role == 'employee':
            self.fields['categories'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))

    def clean(self):
        cleaned_data = super().clean()
        moq = cleaned_data.get('moq')
        if moq is not None and moq < 1:
            self.add_error('moq', "MOQ must be greater than 0")
        return cleaned_data
    
        # if 'categories' in self.data  and  'sub_categories' in self.data:
        #     try:
        #         categories_id = int(self.data.get('categories'))
        #         sub_categories_id = int(self.data.get('sub_categories'))
        #         self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.filter(categories__id=categories_id).order_by('-id')
        #         self.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.filter(sub_categories__id=sub_categories_id).order_by('-id')
        #     except (ValueError, TypeError):
        #         pass 
        
        # elif self.instance.pk:
        #     self.fields['sub_categories'].queryset = admin_dashboard_models.SubCategories.objects.all()
        #     self.fields['sub_sub_categories'].queryset = admin_dashboard_models.SubSubCategories.objects.all()


class ProductVarientForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.ProductVarient
        fields = "__all__"
        exclude = ['product']   
        labels = {
            'sku': "SKU",
            'stock_qty': "Stock Quantity",
            'regular_price': "Regular Selling Price",
            'discount_price': "Price After Discount",
            'cover_photo': "Cover Photo",
            'buying_price': "Actual Item Price",
            'height': "Height in Inch",
            'width': "Width in Inch",
            'weight': "Weights in Grams",
            'sold_count': "Sold Amount",
        }
        widgets = {
            'cover_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'select2 form-control'}),
            'unit': forms.Select(attrs={'class': 'select2 form-control'}),
            'status': forms.Select(attrs={'class': 'select2 form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].empty_label = '--SELECT--'
        self.fields['unit'].empty_label = '--SELECT--'
        

    def clean(self):
        cleaned_data = super().clean()
        discount_price = cleaned_data.get('discount_price')
        regular_price = cleaned_data.get('regular_price')
        height = cleaned_data.get('height')
        weight = cleaned_data.get('weight')
        width = cleaned_data.get('width')

        if discount_price is not None and regular_price is not None:
            if discount_price >= regular_price:
                self.add_error('discount_price', "Discount price must be less than regular price")

        if height is not None and float(height) < 0:
            self.add_error('height', "Please enter positive number")
        
        if weight is not None and float(weight) < 0:
            self.add_error('weight', "Please enter positive number")

        if width is not None and float(width) < 0:
            self.add_error('width', "Please enter positive number")

        return cleaned_data

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.ProductAttribute
        fields = "__all__"
        exclude = ['product', 'product_varient']
        labels = {
            'regular_price': "Regular Price",
            'discount_price': "Discount Price",
            'buying_price': "Buying Price",
        }
        widgets = {
            'color': forms.Select(attrs={'class': 'select2 form-control'}),
            'size': forms.Select(attrs={'class': 'select2 form-control'}),
        }
        

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        if weight is not None and weight < 1:
            self.add_error('weight', "Weight must be greater than 0")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].empty_label = "--SELECT--"
        self.fields['size'].empty_label = "--SELECT--"
        self.fields['color'].required = True
        self.fields['size'].required = True
        self.fields['weight'].required = True
        
        for name, field in self.fields.items():
            if name != 'is_cover':
                field.widget.attrs.update({'class': 'form-control'})

class AddProductAttributeForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.ProductAttribute
        fields = "__all__"
        exclude = ['product', 'product_varient']
        labels = {
            'regular_price': "Regular Price",
            'discount_price': "Discount Price",
            'buying_price': "Buying Price",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].empty_label = "--SELECT--"
        self.fields['size'].empty_label = "--SELECT--"
        self.fields['color'].widget.attrs.update({'class': 'select2 form-control'})
        self.fields['size'].widget.attrs.update({'class': 'select2 form-control'})
        self.fields['weight'].required = True
        self.fields['color'].required = True
        self.fields['size'].required = True

    def clean(self):
        cleaned_data = super().clean()
        regular_price = cleaned_data.get('regular_price')
        discount_price = cleaned_data.get('discount_price')
        weight = cleaned_data.get('weight')

        if discount_price is not None and regular_price is not None:
            if discount_price >=regular_price:
                self.add_error('regular_price', "Regular price must be greater than discount price")

        if weight is not None and weight < 1:
            self.add_error('weight', "Weight must be greater than 0")

        return cleaned_data


class UpdateProductAttributeForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.ProductAttribute
        fields = "__all__"
        exclude = ['product', 'product_varient', 'stock']
        labels = {
            'regular_price': "Regular Price",
            'discount_price': "Discount Price",
            'buying_price': "Buying Price",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].empty_label = "--SELECT--"
        self.fields['size'].empty_label = "--SELECT--"
        self.fields['color'].widget.attrs.update({'class': 'select2 form-control'})
        self.fields['size'].widget.attrs.update({'class': 'select2 form-control'})
        self.fields['weight'].required = True
        self.fields['color'].required = True
        self.fields['size'].required = True

    def clean(self):
        cleaned_data = super().clean()
        regular_price = cleaned_data.get('regular_price')
        discount_price = cleaned_data.get('discount_price')
        weight = cleaned_data.get('weight')

        if discount_price is not None and regular_price is not None:
            if discount_price >=regular_price:
                self.add_error('regular_price', "Regular price must be greater than discount price")

        if weight is not None and weight < 1:
            self.add_error('weight', "Weight must be greater than 0")

        return cleaned_data



# class ProductVarientForm(forms.ModelForm):
#     color = forms.ModelMultipleChoiceField(queryset=admin_dashboard_models.Color.objects.all(), required=False)
#     size = forms.ModelMultipleChoiceField(queryset=admin_dashboard_models.Size.objects.all(), required=False)
#     unit = forms.ModelMultipleChoiceField(queryset=admin_dashboard_models.Unit.objects.all(), required=False)
#     class Meta:
#         model = admin_dashboard_models.ProductVarient
#         fields = "__all__"
#         exclude = ['product']
#         labels = {
#             'product_name': "Product Name",
#             'sku': "SKU",
#             'stock_qty': "Stock Quantity",
#             'regular_price': "Regular Price",
#             'discount_price': "Discount Price",
#             'cover_photo': "Cover Photo",
#             'buying_price': "Buying Price"
#         }
#         widgets = {
#             'color': forms.SelectMultiple(attrs={'class': 'form-control'}),
#             'size': forms.SelectMultiple(attrs={'class': 'form-control'}),
#             'unit': forms.SelectMultiple(attrs={'class': 'form-control'}),
#             'cover_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['brand'].empty_label = '--SELECT--'
#         self.fields['weight'].required = True