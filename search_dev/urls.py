from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("profiles.urls")),
    # path("projects/", include("project.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
