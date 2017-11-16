from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user:
            return False

        return request.user.is_superuser or request.user.id == obj.owner_id
