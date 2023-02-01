from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()


@receiver(post_save, sender=SocialAccount)
def save_social_user_name(sender, instance, created, **kwargs):
    if created:
        # Grabbing data from social account to create profile for that user
        user = User.objects.get(id=instance.user.id)
        profile = Profile.objects.get(user=user)
        user.name = profile.name = instance.extra_data.get("name")
        user.save()
        profile.save()
