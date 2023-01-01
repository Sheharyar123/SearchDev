from django.urls import path

from .views import ProfileListView, ProfileDetailView

app_name = "profiles"

urlpatterns = [
    path("", ProfileListView.as_view(), name="profile_list"),
    path("profile/<uuid:pk>/", ProfileDetailView.as_view(), name="profile_detail"),
]
