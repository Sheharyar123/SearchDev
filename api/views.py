from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db.models import Q
from users.models import Profile, Skill
from projects.models import Project, Tag, Review
from .serializers import (
    ProfileSerializer,
    ProjectSerializer,
    MyTokenObtainPairSerializer,
)
from .permissions import (
    IsProfileOwnerOrReadOnly,
    IsProjectOwnerOrReadOnly,
)


class ProfileList(generics.ListAPIView):
    permission_classes = (IsProfileOwnerOrReadOnly,)
    serializer_class = ProfileSerializer

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


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsProfileOwnerOrReadOnly,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProjectList(generics.ListAPIView):
    permission_classes = (IsProjectOwnerOrReadOnly,)
    serializer_class = ProjectSerializer

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


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsProjectOwnerOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
