from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Skill, Profile, Message

# Register your models here.
class SkillInline(admin.TabularInline):
    """Makes all the skills inline to a project"""

    model = Skill


class ProfileAdmin(admin.ModelAdmin):
    """Shows the admin page for profiles"""

    inlines = [SkillInline]
    list_display = ("user", "headline", "location", "created_on", "updated_on")
    search_fields = ("user", "location", "headline", "bio")
    raw_id_fields = ["user"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message)
