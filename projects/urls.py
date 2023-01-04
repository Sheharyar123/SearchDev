from django.urls import path

from .views import ProjectListView, ProjectDetailView, ProjectCreateView

app_name = "projects"

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("project/<uuid:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("project/create/", ProjectCreateView.as_view(), name="project_create"),
]
