# Generated by Django 4.1.4 on 2023-01-04 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_message_email_alter_message_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
