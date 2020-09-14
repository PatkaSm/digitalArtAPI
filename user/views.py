
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

    @action(detail=False, methods=['post'], url_name='disabled_user', url_path='user/(?P<user_id>\d+)/disabled')
    def disabled_user(self, request, **kwargs):
        disabled_user = get_object_or_404(User, id=kwargs.get('user_id'))
        self.check_object_permissions(request, disabled_user)
        disabled_user.active = False
        return Response(data={'success': 'Pomyślnie dezaktywowano użytkownika'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'delete' or self.action == 'disabled_user':
            self.permission_classes = [IsAdmin]
        if self.action == 'create' or self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]