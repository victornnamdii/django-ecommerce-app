from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .models import Address, Customer


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "address_line",
            "address_line2",
            "city",
            "state",
            "postcode",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Full Name",
            }
        )
        self.fields["phone"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Phone Number",
            }
        )
        self.fields["address_line"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Address Line 1",
            }
        )
        self.fields["address_line2"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Address Line 2",
            }
        )
        self.fields["city"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Town/City/State",
            }
        )
        self.fields["postcode"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Postcode",
            }
        )
        self.fields["country"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Country",
            }
        )
        self.fields["state"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Country",
            }
        )


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(
        label="Enter Name",
        min_length=4,
        max_length=50,
        help_text="Required",
    )
    email = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = Customer
        fields = (
            "name",
            "email",
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Username"}
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control mb-3",
                "placeholder": "E-mail",
                "name": "email",
                "id": "id_email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat Password"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email Address",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email cannot be changed",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "email",
                "id": "form-email",
                "readonly": "readonly",
            }
        ),
    )

    name = forms.CharField(
        label="Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Firstname",
                "id": "form-lastname",
            }
        ),
    )

    class Meta:
        model = Customer
        fields = (
            "email",
            "name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["email"].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "form-email",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "Unfortunately, we can not find that email"
            )
        return email


class PwdResetConfirm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "New Password",
                "id": "form-newpass",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Repeat Password",
                "id": "form-new-pass2",
            }
        ),
    )
