from django.contrib import admin
from .models import Project, Tag, Review

# Register your models here.
class ReviewInline(admin.TabularInline):
    """Makes all the reviews inline to a project"""

    model = Review
    # readonly_fields = ["owner", "value", "body"]


class ProjectAdmin(admin.ModelAdmin):
    """Shows the admin page for projects"""

    inlines = [ReviewInline]
    list_display = ("title", "demo_link", "created_on", "updated_on")
    search_fields = ("title", "description")
    raw_id_fields = ["owner"]


class TagAdmin(admin.ModelAdmin):
    """Shows the admin page for tags"""

    list_display = ("name", "created_on", "updated_on")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag, TagAdmin)
