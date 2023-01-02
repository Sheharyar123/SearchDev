from django import forms

from allauth.account.forms import LoginForm, SignupForm, ResetPasswordKeyForm


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


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    password1.widget.attrs.update(
        {"class": "input input--password", "placeholder": "••••••••"}
    )
    password2.widget.attrs.update(
        {"class": "input input--password", "placeholder": "••••••••"}
    )

    # def __init__(self, *args, **kwargs):
    #     self.fields["password1"].widget = forms.PasswordInput(
    #         attrs={"class": "input input--password", "placeholder": "••••••••"}
    #     )
    #     self.fields["password1"].label = "Change Password"
    #     self.fields["password2"].widget = forms.PasswordInput(
    #         attrs={"class": "input input--password", "placeholder": "••••••••"}
    #     )
    #     self.fields["password2"].label = "Confirm Password"
