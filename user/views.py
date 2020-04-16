
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from user.models import User
from user.permissions import IsAdmin
from user.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_name='register', url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'], url_name='edit_user', url_path='user/(?P<user_id>\d+)/edit')
    def edit_user(self, request, **kwargs):
        user = get_object_or_404(User.objects.filter(id=kwargs.get('user_id')))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.update(instance=request.user, validated_data=serializer.validated_data)
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='user_details', url_path='user/(?P<user_id>\d+)')
    def user_details(self, request, **kwargs):
        user = get_object_or_404(User.objects.filter(id=kwargs.get('user_id')))
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_name='user_delete', url_path='user/(?P<user_id>\d+)/delete')
    def delete_user(self, request, **kwargs):
        user = get_object_or_404(User.objects.filter(id=kwargs.get('user_id')))
        self.check_object_permissions(request, user)
        user.delete()
        return Response(data={'success': 'Pomyślnie usunięto użytkownika', 'user': user.username}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_name='disabled_user', url_path='user/(?P<user_id>\d+)/disabled')
    def disabled_user(self, request, **kwargs):
        disabled_user = get_object_or_404(User, id=kwargs.get('user_id'))
        self.check_object_permissions(request, disabled_user)
        disabled_user.active = False
        return Response(data={'success': 'Pomyślnie dezaktywowano użytkownika'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'edit_user':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'delete_user' or self.action == 'disabled_user':
            self.permission_classes = [IsAdmin]
        if self.action == 'register' or self.action == 'user_details':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]