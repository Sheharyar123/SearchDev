from django.db.models import Q
from django.views.generic import ListView, DetailView

from projects.models import Project
from .models import Profile


class ProfileListView(ListView):
    """View to list all the profiles"""

    model = Profile
    template_name = "profiles/profile_list.html"
    context_object_name = "profile_list"
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            return Profile.objects.filter(
                Q(headline__icontains=query)
                | Q(user__name__icontains=query)
                | Q(location__icontains=query)
                | Q(bio__icontains=query)
            ).distinct()
        else:
            return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


class ProfileDetailView(DetailView):
    """View to display profile in detail"""

    model = Profile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = sorted(
            Project.objects.filter(owner__id=self.get_object().id),
            key=lambda t: (t.vote_ratio, t.vote_count),
            reverse=True,
        )
        return context
