# Generated by Django 4.0.6 on 2022-07-08 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_location_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='social_github',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]