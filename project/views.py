from django.views.generic import ListView, DetailView

from .models import Project

# Create your views here.
class ProjectListView(ListView):
    """Defines the logic to list all projects"""

    model = Project
    template_name = "project/project_list.html"
    context_object_name = "project_list"

    def get_queryset(self):
        return sorted(
            Project.objects.all(),
            key=lambda x: (x.vote_ratio, x.vote_count, x.created_on),
            reverse=True,
        )


class ProjectDetailView(DetailView):
    """Defines the logic to display project in detail"""

    model = Project
    template_name = "project/project_detail.html"
    context_object_name = "project"
