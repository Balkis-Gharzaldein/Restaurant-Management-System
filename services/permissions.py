from rest_framework.permissions import BasePermission
class IsCustomerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff )
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)  

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user  and not request.user.is_superuser and  request.user.is_staff) 
    