from django.shortcuts import render
from django.views.generic import ListView, DetailView

from project.models import Project
from .models import Profile


class ProfileListView(ListView):
    """View to list all the profiles"""

    model = Profile
    template_name = "profiles/profile_list.html"
    context_object_name = "profile_list"


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
