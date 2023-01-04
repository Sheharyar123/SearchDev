from django.urls import path

from .views import (
    UserProfileListView,
    UserProfileDetailView,
    UserAccountView,
    UserAccountEditView,
)

app_name = "users"

urlpatterns = [
    path("", UserProfileListView.as_view(), name="users_profiles"),
    path("profile/<uuid:pk>/", UserProfileDetailView.as_view(), name="user_profile"),
    path("account/", UserAccountView.as_view(), name="user_account"),
    path("account/edit/", UserAccountEditView.as_view(), name="user_account_edit"),
]
