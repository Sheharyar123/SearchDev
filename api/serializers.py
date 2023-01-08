from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import Profile, Skill
from projects.models import Project, Review


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "name",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

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
            "skills",
        ]

    def get_skills(self, profile):
        return SkillSerializer(profile.skills, many=True).data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "body",
        ]


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name="api:profile_detail", read_only=True
    )
    # To show title of each tag instead of id
    tags = serializers.StringRelatedField(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)

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
            "reviews",
            "vote_count",
            "vote_ratio",
        ]

    def get_reviews(self, project):
        return ReviewSerializer(project.reviews, many=True).data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token["id"] = user.id
        token["name"] = user.name
        return token
