from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from projects.models import Project
from .models import Profile, Skill, Message

from .forms import ProfileForm, SkillForm, MessageForm


class UserProfileListView(ListView):
    """View to list all the users"""

    model = Profile
    template_name = "users/users_profiles.html"
    context_object_name = "profile_list"
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            skills = Skill.objects.filter(name__icontains=query)
            return Profile.objects.filter(
                Q(headline__icontains=query)
                | Q(name__icontains=query)
                | Q(location__icontains=query)
                | Q(bio__icontains=query)
                | Q(skills__in=skills)
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
        context["skills"] = self.get_object().skills.exclude(description__exact="")
        context["other_skills"] = self.get_object().skills.filter(description__exact="")
        return context


class UserAccountView(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        return render(request, "users/user_account.html", {"profile": profile})


class UserAccountEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        context = {"form": form}
        return render(request, "users/user_account_edit.html", context)

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = request.user
            user_name = form.cleaned_data["name"]
            user.name = user_name
            user.save()
            form.save()
            messages.success(request, "Your profile was updated successfully.")
        else:
            messages.error(
                request, "There was a problem updating your profile. Please try again!"
            )
        return redirect("users:user_account")


class SkillCreateView(LoginRequiredMixin, CreateView):
    form_class = SkillForm
    template_name = "users/skill_create.html"

    def get_success_url(self):
        messages.success(self.request, "Your skill was added successfully.")
        return reverse_lazy("users:user_account")

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.save()
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = "users/skill_update.html"

    def get_success_url(self):
        messages.success(self.request, "Your skill was updated successfully.")
        return reverse_lazy("users:user_account")


class SkillDeleteView(LoginRequiredMixin, DeleteView):
    model = Skill
    template_name = "users/skill_delete.html"

    def get_success_url(self):
        messages.error(self.request, "Your skill was deleted successfully.")
        return reverse_lazy("users:user_account")


class MessageListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        recipient = request.user.profile
        new_messages = Message.objects.filter(recipient=recipient, is_read=False)
        old_messages = Message.objects.filter(recipient=recipient, is_read=True)
        context = {"new_messages": new_messages, "old_messages": old_messages}
        return render(request, "users/inbox.html", context)


class MessageDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        message = Message.objects.get(id=kwargs["pk"])
        if message.is_read == False:
            message.is_read = True
            message.save()
        context = {"message": message}
        return render(request, "users/message_detail.html", context)


class MessageCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        recipient = Profile.objects.get(id=kwargs.get("pk"))
        form = MessageForm()
        context = {"recipient": recipient, "form": form}
        return render(request, "users/message_create.html", context)

    def post(self, request, *args, **kwargs):
        recipient = Profile.objects.get(id=kwargs.get("pk"))
        try:
            sender = request.user.profile
        except:
            sender = None

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.user.name
                message.email = sender.user.email

            message.save()
            messages.success(request, "Your message was sent.")
        else:
            messages.error(
                request, "There was a problem sending your message. Please try again!"
            )

        return redirect("users:user_profile", pk=recipient.id)
