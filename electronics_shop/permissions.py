from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешение для доступа к ресурсам только для активных сотрудников.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
