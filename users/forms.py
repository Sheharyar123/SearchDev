from django.forms import ModelForm
from .models import Profile, Skill, Message


class ProfileForm(ModelForm):
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


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
