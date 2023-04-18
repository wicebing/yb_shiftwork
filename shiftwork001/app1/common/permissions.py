from rest_framework import permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication, jwt_decode_handler
# from rest_framework_simplejwt.tokens import decode


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            return False