import re
from django import forms
from django.core.exceptions import ValidationError
from pos_app.models import pos_models
from accounts_app.models import User

class BranchForm(forms.ModelForm):
    name = forms.CharField(error_messages={"required": "Branch name is required."})
    address = forms.CharField(error_messages={"required": "Address is required."})

    class Meta:
        model = pos_models.BrachName
        fields = ["name", "address", "contact_no", 'active_status']

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Branch name is required.")

        qs = pos_models.BrachName.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A branch with this name already exists.")

        return name

    def clean_address(self):
        address = self.cleaned_data["address"].strip()
        if not address:
            raise forms.ValidationError("Address is required.")

        qs = pos_models.BrachName.objects.filter(address__iexact=address)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A branch with this address already exists.")

        return address

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r'[0-9০-৯+\-]+', phone):
            raise forms.ValidationError("Phone number can only contain digits")
 
        qs = pos_models.BrachName.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This phone number already exists.")
 
        return phone


class UserSetupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['name','email','phone','pos_role','pos_branch', 'joining_date', 'active_status']
        labels = {
            'pos_role': "Role",
            'pos_branch': "Branch"
        }
        widgets = {
            'gender': forms.Select(attrs={'class': "select2",}),
            'joining_date': forms.DateInput(attrs={'type': "date",}),
            'role': forms.Select(attrs={'class': "select2"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['pos_role'].required = True
        self.fields['pos_branch'].required = True
        self.fields['pos_branch'].empty_label = "--SELECT--"

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r'[0-9০-৯+\-]+', phone):
            raise forms.ValidationError("Phone number can only contain digits")
    
        qs = User.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This phone number already exists.")
    
        return phone


class UserSetupUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','email','phone','pos_role','pos_branch', 'joining_date', 'active_status']
        labels = {
            'pos_role': "Role",
            'pos_branch': "Branch"
        }
        widgets = {
            'gender': forms.Select(attrs={'class': "select2",}),
            'joining_date': forms.DateInput(attrs={'type': "date",}),
            'role': forms.Select(attrs={'class': "select2"}),
            'active_status': forms.CheckboxInput(attrs={'class': "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['pos_role'].required = True
        self.fields['pos_branch'].required = True
        self.fields['pos_branch'].empty_label = "--SELECT--"

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r'[0-9০-৯+\-]+', phone):
            raise forms.ValidationError("Phone number can only contain digits")
    
        qs = User.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This phone number already exists.")
    
        return phone

        # category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=user, employee__role=role).values_list('category', flat=True)
        # if role == 'section_admin' or role == 'employee':
        #     self.fields['category'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))
        # if role == 'section_admin':
        #     self.fields['role'].choices = [('', '--SELECT--'), ('employee', 'Employee')]
        # if role == 'central_admin':
        #     self.fields['role'].choices = [('', '--SELECT--'), ('section_admin', 'Category Admin'), ('employee', 'Employee')]


class CustomerSetupForm(forms.ModelForm):
    class Meta:
        model = pos_models.Customer
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
 
        qs = pos_models.Customer.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email already exists.")
 
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r'[0-9০-৯+\-]+', phone):
            raise forms.ValidationError("Phone number can only contain digits")
    
        qs = pos_models.Customer.objects.filter(phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This phone number already exists.")
    
        return phone
