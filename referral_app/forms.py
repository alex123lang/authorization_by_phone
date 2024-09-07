from django import forms


class PhoneForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label="Номер телефона",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(
        max_length=4,
        label="Код подтверждения",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
