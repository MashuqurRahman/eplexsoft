from django import forms


class SupportForm(forms.Form):

    # name = forms.CharField(
    #     max_length=100,
    #     widget=forms.TextInput(attrs={
    #         "class": "form-control"
    #     })
    # )

    # enlisted_email = forms.EmailField(
    #     widget=forms.EmailInput(attrs={
    #         "class": "form-control"
    #     })
    # )

    # contact_no = forms.CharField(
    #     max_length=20,
    #     widget=forms.TextInput(attrs={
    #         "class": "form-control"
    #     })
    # )

    # business_name = forms.CharField(
    #     required=False,
    #     widget=forms.TextInput(attrs={
    #         "class": "form-control"
    #     })
    # )

    problem_statement = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5
        }),
        label="Message"
    )

    attachment = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control"
        })
    )