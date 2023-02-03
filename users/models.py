from cloudinary.models import CloudinaryField
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
    name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    user_img = CloudinaryField(
        null=True,
        blank=True,
        default="https://res.cloudinary.com/dkfgh093c/image/upload/v1675368559/user-default_m9kpsk.png",
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

    @property
    def imageURL(self):
        try:
            url = self.user_img.url
        except:
            url = ""
        return url


class Skill(models.Model):
    """Skill Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Defines representation of skill object"""
        return self.name


class Message(models.Model):
    """Message Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_read", "-updated_on", "-created_on"]

    def __str__(self):
        return self.subject[:50]

    def get_absolute_url(self):
        """Canonical url for each user message"""
        return reverse("users:message_detail", args=[self.id])
