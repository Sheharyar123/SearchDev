from django import forms
from .models import Review, Project


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]

        labels = {"value": "Place your vote", "body": "Add a comment with your vote"}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "featured_img",
            "description",
            "demo_link",
            "source_link",
        ]

        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
