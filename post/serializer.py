from rest_framework import serializers

from favourites.models import Favourite
from post.models import Post, Comment
from tag.models import Tag
from tag.serializer import TagSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['owner', 'post', 'content', 'date_added']
        read_only_fields = ['owner', 'post']


class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['owner', 'title', 'image', 'describe', 'tag', 'comments']
        read_only_fields = ['owner']

    def create(self, validated_data):
        tags_data = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag = Tag.objects.create(**tag_data)
            post.tag.add(tag)
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tag')
        tags = list(instance.tag.all())
        instance.title = validated_data.get('title', instance.title)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.save()

        for tag_data in tags_data:
            tag = tags.pop(0)
            tag.word = tag_data.get('word', tag_data['word'])
            tag.save()
        return instance

    def get_comments(self, obj):
        offer_comment = Comment.objects.filter(id=obj.id)
        serializer = CommentSerializer(offer_comment, many=True)
        return serializer.data
