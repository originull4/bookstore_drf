from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class AllowAny(BasePermission):

    def has_permission(self, request, view):
        return True


class IsAdminOrReadOnly(BasePermission):
    """
    permission to staff users to GET request
    only superuser users cat access to POST, PUT, DELETE requests
    """
    
    def has_permission(self, request, *args):
        if request.method in SAFE_METHODS: return True
        if request.user.is_superuser: return True
        return False