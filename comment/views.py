from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comment.models import Comment
from comment.serializer import CommentSerializer
from post.models import Post
from user.permissions import IsObjectOwnerOrAdmin


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=['post'], url_name='create_comment', url_path=r'post/(?P<post_id>\d+)/comment')
    def create_comment(self, request, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        self.check_object_permissions(request, post)
        serializer.save(owner=request.user, post=post)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False, url_name='comment_delete',
            url_path=r'post/(?P<post_id>\d+)/comment/(?P<comment_id>\d+)/delete')
    def comment_delete(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        comment = get_object_or_404(Comment, id=kwargs.get('comment_id'), post=post)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(data={'success': 'Pomyślnie usunięto komentarz'}, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False, url_name='comment_edit',
            url_path=r'post/(?P<post_id>\d+)/comment/(?P<comment_id>\d+)/edit')
    def comment_edit(self, request, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        comment = get_object_or_404(Comment, id=kwargs.get('comment_id'), post=post)
        self.check_object_permissions(request, comment)
        serializer.update(comment, serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create_comment':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'comment_delete' or self.action == 'comment_edit':
            self.permission_classes = [IsObjectOwnerOrAdmin]
        return [permission() for permission in self.permission_classes]
