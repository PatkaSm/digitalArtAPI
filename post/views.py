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

    @action(detail=False, methods=['post'], url_name='create', url_path='create')
    def create_post(self, request):
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save(owner=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_name='user_post', url_path='(?P<user_id>\d+)/gallery')
    def my_posts(self, request, **kwargs):
        posts = Post.objects.filter(owner_id=kwargs.get('user_id'))
        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='post_details', url_path='post/(?P<post_id>\d+)')
    def post_details(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        serializer = PostSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_name='edit_post', url_path='post/(?P<post_id>\d+)/edit')
    def post_edit(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(post, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_name='delete_post', url_path='post/(?P<post_id>\d+)/delete')
    def post_delete(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        self.check_object_permissions(request, post)
        post.delete()
        return Response(data={'success': 'Pomyślnie usunięto pracę'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create_post' or self.action == 'my_post':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'post_details':
            self.permission_classes = [AllowAny]
        if self.action == 'delete_post' or self.action == 'edit_post':
            self.permission_classes = [IsObjectOwnerOrAdmin]
        return [permission() for permission in self.permission_classes]



