from rest_framework import serializers

from post.models import Post, Comment
from tag.models import Tag
from tag.serializer import TagSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['owner', 'content', 'date_added']


class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['owner', 'title', 'image', 'describe', 'tag', 'comments']

    def create(self, validated_data):
        tags_data = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag = Tag.objects.create(**tag_data)
            post.tag.add(tag)
        return post

    def get_comments(self, obj):
        offer_comment = Comment.objects.filter(id=obj.id)
        serializer = CommentSerializer(offer_comment, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tag')
        tag = instance.tag
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.describe = validated_data.get('describe', instance.describe)
        for tag_data in tags_data:
            tag.word = tag_data.get('word', tag_data)
            tag.save()
        return instance


