from django import forms
from .models import Profile, Skill, Message


class ProfileForm(forms.ModelForm):
    user_img = forms.ImageField(
        label="Profile Pic",
        required=False,
        error_messages={"invalid": "Image files only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = Profile
        fields = [
            "name",
            "headline",
            "bio",
            "location",
            "user_img",
            "social_github",
            "social_twitter",
            "social_linkedin",
            "social_youtube",
            "social_website",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
