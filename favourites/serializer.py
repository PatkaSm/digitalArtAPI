from rest_framework import serializers

from favourites.models import Favourite


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ['user', 'post']
