# Generated by Django 3.0.5 on 2020-06-20 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_post_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
