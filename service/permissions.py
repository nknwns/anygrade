from rest_framework import permissions

OWNER_METHODS = ('PUT', 'DELETE', 'PATH')
CREATOR_METHODS = ('POST',)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdminOrAuthorUpdateAndDeleteOrCreatorCreateOrAuthenticatedRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in CREATOR_METHODS:
            return bool(
                request.user.status == 'creator'
            )

        if request.method in OWNER_METHODS:
            return bool(
                request.user.status == 'creator' and
                request.user == obj.author
            )
