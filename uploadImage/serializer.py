from rest_framework import serializers

from uploadImage.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'post', 'img']
