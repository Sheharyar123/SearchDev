from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from projects.models import Project
from .models import Profile

from .forms import ProfileForm


class UserProfileListView(ListView):
    """View to list all the users"""

    model = Profile
    template_name = "users/users_profiles.html"
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
            return Profile.objects.exclude(headline__exact=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


class UserProfileDetailView(DetailView):
    """View to display profile in detail"""

    model = Profile
    template_name = "users/user_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = sorted(
            Project.objects.filter(owner__id=self.get_object().id),
            key=lambda t: (t.vote_ratio, t.vote_count),
            reverse=True,
        )
        return context


class UserAccountView(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        return render(request, "users/user_account.html", {"profile": profile})


class UserAccountEditView(View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, "users/user_account_edit.html", {"form": form})

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            return redirect("users:user_account")
