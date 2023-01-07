from rest_framework import serializers
from users.models import Profile
from projects.models import Project


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
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


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedIdentityField(
        view_name="api:profile_detail", format="html"
    )
    # To show title of each tag instead of id
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "owner",
            "tags",
            "title",
            "description",
            "demo_link",
            "source_link",
            "featured_img",
        ]
