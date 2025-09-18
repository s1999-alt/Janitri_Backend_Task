from rest_framework import permissions

# class IsDoctorOrReadOnly(permissions.BasePermission):
#   def has_permission(self, request, view):
#     if request.method in permissions.SAFE_METHODS:
#       return request.user and request.user.is_authenticated
#     return request.user and request.user.is_authenticated and (request.user.role in ['doctor','nurse','admin'])

class IsAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.role == 'admin'
  
class IsDoctor(permissions.BasePermission):
   def has_permission(self, request, view):
     return request.user.is_authenticated and request.user.role == 'doctor'
   
class IsNurse(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.role == 'nurse'

class IsAdminOrDoctor(permissions. BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.role in ['admin', 'doctor']