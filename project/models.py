from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.
class Tag(models.Model):
    """Tag Model"""

    name = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Defines representation of a tag object"""
        return self.name


class Project(models.Model):
    """Project Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # owner = models.ForeignKey(
    #     get_user_model(), on_delete=models.SET_NULL, null=True, related_name="projects"
    # )
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    demo_link = models.CharField(max_length=255, unique=True, null=True, blank=True)
    source_code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    featured_img = models.ImageField(
        upload_to="photos/projects", null=True, blank=True, default="default.jpg"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_on", "-created_on"]
        indexes = [models.Index(fields=["id", "-updated_on", "-created_on"])]

    def __str__(self):
        """Defines representation of a project object"""
        return self.title

    @property
    def vote_ratio(self):
        """Returns the ratio of positive votes"""
        total_votes = self.reviews.count()
        up_votes = self.reviews.filter(value__iexact="Up Vote").count()
        return round((up_votes / total_votes) * 100, 0)

    @property
    def vote_count(self):
        """Returns the total votes based on users feedback"""
        return self.reviews.count()


class Review(models.Model):
    """Review Model"""

    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="reviews"
    )
    # owner = models.OneToOneField(get_user_model(), on_delete=)
    value = models.CharField(max_length=4, choices=VOTE_TYPE)
    body = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_on", "-created_on"]
        indexes = [models.Index(fields=["id", "-updated_on", "-created_on"])]
        unique_together = [["owner", "project"]]

    def __str__(self):
        """Defines representation of a review object"""
        return self.value
