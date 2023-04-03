from rest_framework.permissions import BasePermission

class IsObjectOwner(BasePermission):
    """
    This permission is used to check obj.user == request.user
    This is a common class can be used
    """
    message = 'You do not have permission to access this object'
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
