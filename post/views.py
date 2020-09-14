from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from post.models import Post
from post.serializer import PostSerializer
from user.permissions import IsObjectOwnerOrAdmin


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['get'], url_name='user_post', url_path='(?P<user_id>\d+)/gallery')
    def my_posts(self, request, **kwargs):
        posts = get_object_or_404(Post.objects.filter(owner_id=kwargs.get('user_id')))
        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'my_post':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update' \
                or self.action == 'list':
            self.permission_classes = [IsObjectOwnerOrAdmin]
        return [permission() for permission in self.permission_classes]



