from django.urls import path

from .views import (
    UserProfileListView,
    UserProfileDetailView,
    UserAccountView,
    UserAccountEditView,
    CreateSkillView,
    UpdateSkillView,
    DeleteSkillView,
)

app_name = "users"

urlpatterns = [
    path("", UserProfileListView.as_view(), name="users_profiles"),
    path("profile/<uuid:pk>/", UserProfileDetailView.as_view(), name="user_profile"),
    path("account/", UserAccountView.as_view(), name="user_account"),
    path("account/edit/", UserAccountEditView.as_view(), name="user_account_edit"),
    path("create/skill/", CreateSkillView.as_view(), name="create_skill"),
    path("update/skill/<uuid:pk>/", UpdateSkillView.as_view(), name="update_skill"),
    path("delete/skill/<uuid:pk>/", DeleteSkillView.as_view(), name="delete_skill"),
]
