from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                )


class IsUserOrAdminOrModerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.author == request.user
                    or request.user.is_moderator
                    or request.user.is_admin)
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
            )
        )
