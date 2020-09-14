from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favourites.models import Favourite
from favourites.serializer import FavouriteSerializer
from post.models import Post
from user.permissions import IsAdmin


class FavouriteViewSet(mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def create(self, request, **kwargs):
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
        if self.action == 'my_favourites' or self.action == 'create':
            self.permission_classes = [IsAuthenticated]

        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update' \
                or self.action == 'retrieve':
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]
