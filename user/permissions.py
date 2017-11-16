from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if not request.user:
            return False

        return request.is_admin or request.user.is_superuser\
            or request.user.id == obj.id
