# Generated by Django 4.1.4 on 2023-01-04 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('headline', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('user_img', models.ImageField(blank=True, default='photos/profiles/user-default.png', null=True, upload_to='photos/profiles')),
                ('social_github', models.CharField(blank=True, max_length=255, null=True)),
                ('social_twitter', models.CharField(blank=True, max_length=255, null=True)),
                ('social_linkedin', models.CharField(blank=True, max_length=255, null=True)),
                ('social_youtube', models.CharField(blank=True, max_length=255, null=True)),
                ('social_website', models.CharField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_on', '-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='users.profile')),
            ],
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['id', '-updated_on', '-created_on'], name='users_profi_id_4f1319_idx'),
        ),
    ]
