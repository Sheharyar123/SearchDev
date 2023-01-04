from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
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
