# Generated by Django 4.1.4 on 2023-01-07 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_message_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]