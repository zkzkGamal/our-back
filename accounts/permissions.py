from rest_framework import permissions

class onlyUnAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class AUTH_READ_ONLY(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or (request.method in permissions.SAFE_METHODS)

class AUTH_ONLY(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
class DoctorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Doctors").exists()
        ) or (request.method in permissions.SAFE_METHODS)