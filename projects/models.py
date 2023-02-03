import uuid
from cloudinary.models import CloudinaryField
from django.db import models
from django.urls import reverse
from users.models import Profile

# Create your models here.
class Tag(models.Model):
    """Tag Model"""

    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Defines representation of a tag object"""
        return self.name


class Project(models.Model):
    """Project Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name="projects"
    )
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    demo_link = models.CharField(max_length=255, null=True, blank=True)
    source_link = models.CharField(max_length=255, null=True, blank=True)
    featured_img = CloudinaryField(
        null=True,
        blank=True,
        default="https://res.cloudinary.com/dkfgh093c/image/upload/v1675368588/default_fsuwsb.jpg",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["id", "-updated_on", "-created_on"])]

    def __str__(self):
        """Defines representation of a project object"""
        return self.title

    def get_absolute_url(self):
        """Canonical url for each user project"""
        return reverse("projects:project_detail", args=[self.id])

    @property
    def vote_count(self):
        """Returns the total votes based on users feedback"""
        return self.reviews.count()

    @property
    def vote_ratio(self):
        """Returns the ratio of positive votes"""
        total_votes = self.vote_count
        up_votes = self.reviews.filter(value__iexact="up").count()
        print(up_votes)
        if total_votes == 0 or up_votes == 0:
            return 0
        return round(up_votes / total_votes * 100)

    @property
    def imageURL(self):
        try:
            url = self.featured_img.url
        except:
            url = ""
        return url

    @property
    def reviewers(self):
        queryset = self.reviews.all().values_list("owner__id", flat=True)
        return queryset


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
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reviews")
    value = models.CharField(max_length=4, choices=VOTE_TYPE)
    body = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_on", "-created_on"]
        indexes = [models.Index(fields=["id", "-updated_on", "-created_on"])]
        unique_together = [["owner", "project"]]

    def __str__(self):
        """Defines representation of a review object"""
        return self.value
