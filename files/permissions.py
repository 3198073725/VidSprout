from rest_framework import permissions

from .methods import is_mediacms_editor, is_mediacms_manager


class IsMediacmsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_mediacms_editor(request.user):
            return True
        return False


class IsMediacmsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_mediacms_manager(request.user):
            return True
        return False
