from django.shortcuts import render
from django.views.generic import ListView

from .models import Profile


class ProfileListView(ListView):
    """View to list all the profiles"""

    model = Profile
    template_name = "profiles/profile_list.html"
    context_object_name = "profile_list"
