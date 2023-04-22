from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin or if the user is the owner of the object
        return request.user.is_superuser or request.user == obj or request.user.table_staff == obj