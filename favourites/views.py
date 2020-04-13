from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favourites.models import Favourite
from favourites.serializer import FavouriteSerializer
from post.models import Post


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    @action(detail=False, methods=['post'], url_name='add_or_remove', url_path='add/(?P<offer_id>\d+)')
    def add_or_remove(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('offer_id'))
        try:
            fav_offer = Favourite.objects.get(post=post, user=request.user)
        except Favourite.DoesNotExist:
            Favourite.objects.create(post=post, user=request.user)
            return Response(data={'success': 'Dodano pracę do ulubionych!'}, status=status.HTTP_201_CREATED)
        fav_offer.delete()
        return Response(data={'success': 'Usunięto pracę z ulubionych!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='user_fav_posts', url_path='my_favourites')
    def my_favourites(self, request):
        fav_posts = Favourite.objects.filter(user=request.user)
        serializer = FavouriteSerializer(fav_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'my_favourites' or self.action == 'add_or_remove':
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]