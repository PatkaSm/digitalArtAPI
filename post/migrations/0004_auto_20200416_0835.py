# Generated by Django 3.0.5 on 2020-04-16 08:35

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200416_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=post.models.upload_location),
        ),
    ]
