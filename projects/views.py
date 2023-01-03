from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from .forms import ReviewForm
from .models import Project, Review

# Create your views here.
class ProjectListView(ListView):
    """Defines the logic to list all projects"""

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "project_list"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return sorted(
                Project.objects.filter(
                    Q(title__icontains=query)
                    | Q(owner__user__name__icontains=query)
                    | Q(tags__name__icontains=query)
                    | Q(description__icontains=query)
                ).distinct(),
                key=lambda x: (x.vote_ratio, x.vote_count, x.created_on),
                reverse=True,
            )
        else:
            return sorted(
                Project.objects.all(),
                key=lambda x: (x.vote_ratio, x.vote_count, x.created_on),
                reverse=True,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


class ProjectDetailView(DetailView):
    """Defines the logic to display project in detail"""

    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        owner = self.request.user.profile
        context["commented"] = Review.objects.filter(
            owner=owner, project=self.get_object()
        ).exists()
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.project = self.get_object()
            review.save()
            return redirect(self.get_object().get_absolute_url())
        else:
            return None
