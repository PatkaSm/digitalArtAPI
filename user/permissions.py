from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Dozwolone tylko dla administratora.'

    def has_permission(self, request, view):
        return request.user.is_staff


class IsAdminOrOwner(permissions.BasePermission):
    message = 'Dozwolone tylko dla administratora.'

    def has_permission(self, request, view):
        return request.user.is_staff


class IsObjectOwnerOrAdmin(permissions.BasePermission):
    message = "Dozwolone tylko dla autora lub admina."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff



