# Generated by Django 3.0.5 on 2020-07-14 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('post', '0009_auto_20200711_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(to='tag.Tag'),
        ),
    ]
