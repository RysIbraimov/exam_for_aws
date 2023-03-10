from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    request.user and request.user.is_authenticated and
                    request.user.author)

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or
                    request.user and request.user.is_authenticated and
                    request.user.author == obj.author)
