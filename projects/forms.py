from django.forms import ModelForm, CheckboxSelectMultiple, ImageField, FileInput
from .models import Review, Project


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["body", "value"]

        labels = {"value": "Place your vote", "body": "Add a comment with your vote"}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ProjectForm(ModelForm):
    featured_img = ImageField(
        label="Featured Image",
        required=False,
        error_messages={"invalid": "Image files only"},
        widget=FileInput,
    )

    class Meta:
        model = Project
        fields = ["title", "featured_img", "description", "demo_link", "source_link"]
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
