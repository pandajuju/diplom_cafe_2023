# Generated by Django 5.0 on 2024-01-09 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0002_remove_tag_posts_post_posts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='posts',
            new_name='tags',
        ),
    ]