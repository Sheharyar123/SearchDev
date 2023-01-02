from django import forms

from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields["login"].widget = forms.TextInput(
            attrs={
                "type": "email",
                "class": "input input--text",
                "placeholder": "Enter your email...",
            }
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "input input--password", "placeholder": "••••••••"}
        )


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=255, label="Full Name")

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget = forms.TextInput(
            attrs={
                "type": "text",
                "class": "input input--text",
                "placeholder": "e.g. Sheharyar Ahmad",
            }
        )
        self.fields["email"].widget = forms.TextInput(
            attrs={
                "type": "email",
                "class": "input input--text",
                "placeholder": "e.g. user@domain.com",
            }
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "input input--password", "placeholder": "••••••••"}
        )
        self.fields["password1"].label = "Password"
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "input input--password", "placeholder": "••••••••"}
        )
        self.fields["password2"].label = "Confirm Password"

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data["name"]
        user.save()
