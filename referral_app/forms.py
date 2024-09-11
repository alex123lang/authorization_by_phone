from django import forms
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

from referral_app.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if not phone_number.isdigit():
            raise ValidationError("Номер телефона должен содержать только цифры")
        return phone_number


class AuthCodeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["auth_code"]

    def clean_auth_code(self):
        user = self.instance
        auth_code = self.cleaned_data["auth_code"]
        if auth_code != str(self.instance.auth_code):
            raise ValidationError("Неверный код")
        user.auth_code = None
        user.save()
        return auth_code


class InviteCodeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["invite_used"]
        labels = {
            "invite_used": "Enter Invite Code",
        }

    def clean_invite_used(self):
        invite_used = self.cleaned_data.get("invite_used")
        if (
            invite_used
            and not UserProfile.objects.filter(invite_code=invite_used).exists()
        ):
            raise forms.ValidationError("This invite code is invalid.")
        return invite_used
