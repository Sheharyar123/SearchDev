# Generated by Django 4.1.4 on 2023-01-02 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-updated_on', '-created_on']},
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['id', '-updated_on', '-created_on'], name='profiles_pr_id_3a1e78_idx'),
        ),
    ]
