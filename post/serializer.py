from rest_framework import serializers

from post.models import Post, Comment
from tag.models import Tag
from tag.serializer import TagSerializer
from uploadImage.models import Image
from uploadImage.serializer import ImageSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['owner', 'post', 'content', 'date_added']
        read_only_fields = ['owner', 'post']


class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()
    images_list = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'images_list', 'describe', 'tag', 'comments']
        read_only_fields = ['owner']

    def get_comments(self, obj):
        offer_comment = Comment.objects.filter(id=obj.id)
        serializer = CommentSerializer(offer_comment, many=True)
        return serializer.data

    def get_images_list(self, obj):
        post_images = Image.objects.filter(post=obj.id)
        serializer = ImageSerializer(post_images, many=True)
        images = []
        for img in serializer.data:
            images.append(('http://' + self.context['request'].get_host() + img['img']))
        return images

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


