from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if not request.user:
            return False

        if request.method != "DELETE":
            return request.user.is_superuser\
                or request.user.id == obj.id
        else:
            return request.user.is_superuser
        
