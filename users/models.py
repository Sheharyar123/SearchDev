from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid


class Profile(models.Model):
    """Model for User Profile"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )
    headline = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    user_img = models.ImageField(
        upload_to="photos/profiles",
        null=True,
        blank=True,
        default="photos/profiles/user-default.png",
    )
    social_github = models.CharField(max_length=255, null=True, blank=True)
    social_twitter = models.CharField(max_length=255, null=True, blank=True)
    social_linkedin = models.CharField(max_length=255, null=True, blank=True)
    social_youtube = models.CharField(max_length=255, null=True, blank=True)
    social_website = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_on", "-created_on"]
        indexes = [models.Index(fields=["id", "-updated_on", "-created_on"])]

    def __str__(self):
        """Defines representation of profile object"""
        return f"{self.user.name}'s profile"

    def get_absolute_url(self):
        """Canonical url for each user profile"""
        return reverse("users:user_profile", args=[self.id])


class Skill(models.Model):
    """Skill Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Defines representation of skill object"""
        return self.name
