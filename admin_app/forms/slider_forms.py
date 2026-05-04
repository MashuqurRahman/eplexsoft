from django import forms
from admin_app.models import admin_dashboard_models
from accounts_app.models import User

class SideSliderForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.SideSlider
        fields = ['campaign_name', 'image',  'campaign_type', 'start_date', 'end_date']
        labels = {
            'campaign_name': "Campaign Name",
            'campaign_type': "Campaign Type",
            'start_date': "Start Date",
            'end_date': "End Date",
        }
        widgets = {
            # 'product': forms.Select(attrs={'class': 'select2 form-control'}),
            # 'side_slider': forms.Select(attrs={'class': 'select2 form-control'}),
            'campaign_type': forms.Select(attrs={'class': 'select2 form-control'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date >= end_date:
            self.add_error('end_date', "End date must be after start date.")
        return cleaned_data



class SliderForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Slider
        fields = ['name', 'image', 'slider_url', 'is_active']
        labels = {
            'slider_url': "Slider URL"
        }

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )
    category = forms.ModelMultipleChoiceField(queryset=admin_dashboard_models.Categories.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2'}))

    class Meta:
        model = User
        fields = ['name','email','phone','gender','role','category']
        widgets = {
            'gender': forms.Select(attrs={'class': "select2"}),
            'role': forms.Select(attrs={'class': "select2"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['gender'].required = True
        self.fields['role'].required = True

        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=user, employee__role=role).values_list('category', flat=True)
        if role == 'section_admin' or role == 'employee':
            self.fields['category'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))
        if role == 'section_admin':
            self.fields['role'].choices = [('', '--SELECT--'), ('employee', 'Employee')]
        if role == 'central_admin':
            self.fields['role'].choices = [('', '--SELECT--'), ('section_admin', 'Category Admin'), ('employee', 'Employee')]


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class EmployeeUpdateForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=admin_dashboard_models.Categories.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2'}))
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'gender', 'role', 'category']
        widgets = {
            'gender': forms.Select(attrs={'class': "select2"}),
            'role': forms.Select(attrs={'class': "select2"}),
            'category': forms.Select(attrs={'class': "select2"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=user, employee__role=role).values_list('category', flat=True)
        if role == 'section_admin' or role == 'employee':
            self.fields['category'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))
        if role == 'section_admin':
            self.fields['role'].choices = [('', '--SELECT--'), ('employee', 'Employee')]
        if role == 'central_admin':
            self.fields['role'].choices = [('', '--SELECT--'), ('section_admin', 'Category Admin'), ('employee', 'Employee')]
        
            
        for field_name in ['name', 'phone', 'gender', 'role']:
            if field_name in self.fields:
                self.fields[field_name].required = True


class CourierForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Courier
        fields = "__all__"
        labels = {
            'api_key': "API Key",
            'secret_key': "Secret Key",
            'base_url': "Base URL"
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        if status:
            courier_obj = admin_dashboard_models.Courier.objects.filter(status=True)
            if self.instance.pk:
                courier_obj = courier_obj.exclude(pk=self.instance.pk)
            if courier_obj.exists():
                self.add_error('status',"Another active courier already exists.")
        return cleaned_data
    
class CourierUpdateForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.Courier
        fields = "__all__"
        labels = {
            'api_key': "API Key",
            'secret_key': "Secret Key",
            'base_url': "Base URL"
        }


class PathaoCourierForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.PathaoCourier
        fields = "__all__"
        labels = {
            'api_key': "API Key",
            'secret_key': "Secret Key",
            'base_url': "Base URL",
            'store_id': "Store Id",
            'zone_id': "Zone Id",
            'city_id': "City Id",
            'area_id': "Area Id",
        }

class RedxCourierForm(forms.ModelForm):
    class Meta:
        model = admin_dashboard_models.RedxCourier
        fields = "__all__"
        labels = {
            'base_url': "Base URL",
            'api_key': "API Key",
            'pickup_store_id': "Pickup Store Id",
            'pickup_phone': "Pickup Phone"
        }