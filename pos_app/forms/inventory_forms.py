from django import forms
from pos_app.models import pos_models

class SupplierForm(forms.ModelForm):
    class Meta:
        model = pos_models.Supplier
        fields = "__all__"
        widgets = {
            'address': forms.TextInput(attrs={'rows': 1, 'cols': 1})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "--SELECT--"