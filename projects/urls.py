from django.urls import path

from .views import ProjectListView, ProjectDetailView

app_name = "project"

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("project/<uuid:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
