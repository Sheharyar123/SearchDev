from django.urls import path

from .views import (
    UserProfileListView,
    UserProfileDetailView,
    UserAccountView,
    UserAccountEditView,
    SkillCreateView,
    SkillUpdateView,
    SkillDeleteView,
    MessageCreateView,
    MessageListView,
    MessageDetailView,
)

app_name = "users"

urlpatterns = [
    path("", UserProfileListView.as_view(), name="users_profiles"),
    path("profile/<uuid:pk>/", UserProfileDetailView.as_view(), name="user_profile"),
    path("account/", UserAccountView.as_view(), name="user_account"),
    path("account/edit/", UserAccountEditView.as_view(), name="user_account_edit"),
    path("create/skill/", SkillCreateView.as_view(), name="skill_create"),
    path("update/skill/<uuid:pk>/", SkillUpdateView.as_view(), name="skill_update"),
    path("delete/skill/<uuid:pk>/", SkillDeleteView.as_view(), name="skill_delete"),
    path("create/message/", MessageCreateView.as_view(), name="message_create"),
    path("inbox/", MessageListView.as_view(), name="inbox"),
    path("message/<uuid:pk>/", MessageDetailView.as_view(), name="message_detail"),
]
