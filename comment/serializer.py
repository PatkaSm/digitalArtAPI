from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['owner', 'post', 'content', 'date_added']
        read_only_fields = ['owner', 'post']

    def create(self, validated_data):
        return Comment.objects.create(owner=self.context['request'].user, **validated_data)


