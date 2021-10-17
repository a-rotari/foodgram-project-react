from rest_framework.permissions import SAFE_METHODS, BasePermission


class RecipePermission(BasePermission):
    """
    This custom permission class is intended to be used for handling Recipe
    objects.
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_active)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
