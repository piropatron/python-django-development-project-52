from django  import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordMixin


class UserForm(SetPasswordMixin, forms.ModelForm):
    password1, password2 = SetPasswordMixin.create_password_fields()

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
    password1, password2 = SetPasswordMixin.create_password_fields()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            'password1',
            'password2',
        ]
