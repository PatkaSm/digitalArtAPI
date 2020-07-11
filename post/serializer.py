from rest_framework import serializers

from comment.models import Comment
from comment.serializer import CommentSerializer
from favourites.models import Favourite
from post.models import Post
from tag.models import Tag
from tag.serializer import TagSerializer


class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'image', 'title',  'describe', 'tag', 'comments', 'is_favourite', 'likes']
        read_only_fields = ['owner']

    def get_comments(self, obj):
        offer_comment = Comment.objects.filter(id=obj.id)
        serializer = CommentSerializer(offer_comment, many=True)
        return serializer.data

    def get_is_favourite(self, obj):
        if self.context['request'].user.is_authenticated:
            is_favourite = Favourite.objects.filter(post=obj.id, user=self.context['request'].user)
            if is_favourite.exists():
                return True
        return False

    def likes(self, obj):
        is_favourite = Favourite.objects.filter(post=obj.id)
        likes = is_favourite.count()
        return likes

    def create(self, validated_data):
        tags_data = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            used_tag = Tag.objects.filter(word=tag_data['word'])
            if used_tag.exists():
                post.tag.add(used_tag[0])
            else:
                tag = Tag.objects.create(**tag_data)
                post.tag.add(tag)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.save()

        if 'tag' in validated_data.keys():
            tags_data = validated_data.pop('tag')
            instance.tag.clear()

            for tag_data in tags_data:
                tag = Tag.objects.create(**tag_data)
                instance.tag.add(tag)

        return instance


