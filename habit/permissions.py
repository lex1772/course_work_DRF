from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # Класс для скрытия привычек пользователя
    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.user.pk:
            return True
        else:
            return False


class IsPublic(permissions.BasePermission):
    # Класс для скрытия привычек пользователя, если они не публичные
    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.user.pk or obj.is_public is True:
            return True
        else:
            return False
