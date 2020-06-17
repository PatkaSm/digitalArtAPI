from django.db import models

from tag.models import Tag
from user.models import User


def upload_location(instance, filename):
    return "photo %s/%s" %(instance.owner, filename)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    describe = models.TextField(max_length=500, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date_added = models.DateField(auto_now=True)