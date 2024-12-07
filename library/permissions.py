from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET',):
            return True
        return request.user and request.user.is_staff

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_staff
