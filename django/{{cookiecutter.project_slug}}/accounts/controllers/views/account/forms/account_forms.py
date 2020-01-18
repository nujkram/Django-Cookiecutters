from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, SetPasswordForm, \
    ReadOnlyPasswordHashField

from accounts.models import Account


class LoginForm(AuthenticationForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ("username", "password")


class CompanyUserRegistrationForm(UserCreationForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=
            f"Raw passwords are not stored, so there is no way to see this "
            f"user's password, but you can change the password using "
            f"<a href='/profile/account/password'>this form</a>."
    )
    class Meta:
        model = Account
        fields = (
            "username",
            "email",
            "password"
        )


class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = Account
        fields = (
            'username',
            'email'
        )


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ("password", "confirm_password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Your passwords don't match!")

