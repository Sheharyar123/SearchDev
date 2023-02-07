import re
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ReviewForm, ProjectForm
from .models import Project, Tag

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
            tags = Tag.objects.filter(name__icontains=query)
            return sorted(
                Project.objects.filter(
                    Q(title__icontains=query)
                    | Q(owner__user__name__icontains=query)
                    | Q(tags__name__icontains=query)
                    | Q(description__icontains=query)
                    | Q(tags__in=tags)
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
        context["form"] = ReviewForm
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.project = self.get_object()
            review.save()
            messages.success(request, "Your review was submitted")
            return redirect(self.get_object().get_absolute_url())


class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        context = {"form": form}
        return render(request, "projects/project_create.html", context)

    def post(self, request, *args, **kwargs):
        newtags = request.POST.get("newtags").split(",")
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            messages.success(request, "Your project was added successfully.")

            for tag in newtags:
                valid_tag = re.search("[a-zA-Z0-9#+$()]+", tag)
                if valid_tag:
                    name = tag.lower()
                    tag, created = Tag.objects.get_or_create(name=name)
                    project.tags.add(tag)
        else:
            messages.error(
                request, "There was a problem adding your project. Please try again!"
            )
        return redirect("users:user_account")


class ProjectUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs["pk"])
        tags = ",".join([tag.name for tag in project.tags.all()])
        form = ProjectForm(instance=project)
        context = {"form": form, "project": project, "tags": tags}
        return render(request, "projects/project_update.html", context)

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs["pk"])
        newtags = request.POST.get("newtags").split(",")
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            messages.success(request, "Your project was updated successfully.")

            for tag in newtags:
                valid_tag = re.search("[a-zA-Z0-9#+$()]+", tag)
                if valid_tag:
                    name = tag.lower()
                    try:
                        check_tag = Tag.objects.get(name=name)
                    except Tag.DoesNotExist:
                        tag = Tag.objects.create(name=name)
                        project.tags.add(tag)
        else:
            messages.error(
                request, "There was a problem updating your project. Please try again!"
            )
        return redirect("users:user_account")


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_delete.html"

    def get_success_url(self):
        messages.error(self.request, "Your project was deleted successfully.")
        return reverse_lazy("users:user_account")
