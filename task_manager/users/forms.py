from django import forms
from django.contrib.auth.forms import SetPasswordMixin, UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):
    #password1, password2 = SetPasswordMixin.create_password_fields()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            'password1',
            'password2',
        ]


class UserChangeForm(SetPasswordMixin, forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            'password1',
            'password2',
        ]
