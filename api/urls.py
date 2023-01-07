from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ProfileList, ProfileDetail, ProjectList, ProjectDetail

app_name = "api"

urlpatterns = format_suffix_patterns(
    [
        path("profiles/", ProfileList.as_view(), name="profile_list"),
        path("profile/<uuid:pk>/", ProfileDetail.as_view(), name="profile_detail"),
        path("projects/", ProjectList.as_view(), name="project_list"),
        path("project/<uuid:pk>/", ProjectDetail.as_view(), name="project_detail"),
    ]
)
