from django import forms
from pos_app.models import pos_models
from accounts_app.models import User

class BranchForm(forms.ModelForm):
    name = forms.CharField(error_messages={"required": "Branch name is required."})
    address = forms.CharField(error_messages={"required": "Address is required."})
    
    class Meta:
        model = pos_models.BrachName
        fields = ["name", "address", "contact_no"]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Branch name is required.")
        return name

    def clean_address(self):
        address = self.cleaned_data["address"].strip()
        if not address:
            raise forms.ValidationError("Address is required.")
        return address


class UserSetupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['name','email','phone','gender','pos_role','pos_branch']
        labels = {
            'pos_role': "Role",
            'pos_branch': "Branch"
        }
        widgets = {
            'gender': forms.Select(attrs={'class': "select2",}),
            'role': forms.Select(attrs={'class': "select2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['gender'].required = True
        self.fields['pos_role'].required = True
        self.fields['pos_branch'].required = True
        self.fields['pos_branch'].empty_label = "--SELECT--"

        # category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee=user, employee__role=role).values_list('category', flat=True)
        # if role == 'section_admin' or role == 'employee':
        #     self.fields['category'].queryset = admin_dashboard_models.Categories.objects.filter(id__in=list(category_ids))
        # if role == 'section_admin':
        #     self.fields['role'].choices = [('', '--SELECT--'), ('employee', 'Employee')]
        # if role == 'central_admin':
        #     self.fields['role'].choices = [('', '--SELECT--'), ('section_admin', 'Category Admin'), ('employee', 'Employee')]


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