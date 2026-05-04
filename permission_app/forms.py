from django import forms
from accounts_app.models import User
from admin_app.models import admin_dashboard_models
from .models import AdminPanelPermissions

class AdminPanelPermissionForm(forms.ModelForm):
    class Meta:
        model = AdminPanelPermissions
        fields = ['user', 'permission']
        widgets = {
            'user': forms.Select(attrs={'class': 'select2 form-control'}),
            'permission': forms.Select(attrs={'class': 'select2 form-control'}),
        }

    def __init__(self, *args, **kwargs):
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = "--SELECT--"

        if role == 'section_admin':
            category_ids = admin_dashboard_models.EmployeeCategories.objects.filter(employee__role='section_admin').values_list('category', flat=True)
            self.fields['user'].queryset = User.objects.filter(role='employee', employee_of_category__category_id__in=list(category_ids)).distinct()
        if role == 'central_admin':
            self.fields['user'].queryset = User.objects.filter(role__in=['section_admin', 'employee'])

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        permission = cleaned_data.get('permission')

        if user and permission:
            if AdminPanelPermissions.objects.filter(
                user=user, permission=permission
            ).exists():
                # This attaches the error directly to the permission field
                self.add_error('permission', "This permission already exists for the selected user.")
                
        return cleaned_data