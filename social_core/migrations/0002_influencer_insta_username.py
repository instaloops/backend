# Generated by Django 3.2.3 on 2021-05-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='insta_username',
            field=models.CharField(blank=True, max_length=54, null=True),
        ),
    ]