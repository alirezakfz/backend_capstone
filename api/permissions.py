from rest_framework.permissions import BasePermission

class MenuItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name = 'Manager').exists():
                if request.method in ["GET","POST","PATCH"]:
                    return True
            elif (request.user.groups.filter(name = 'Delivery').exists() | request.user.groups.filter(name = 'Customer').exists()) and request.method == "GET":
                return True
        return False



class SingleMenuItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name = 'Manager').exists():
                if request.method in ["GET","POST","PATCH", "DELETE"]:
                    return True
            elif (request.user.groups.filter(name = 'Delivery').exists() | request.user.groups.filter(name = 'Customer').exists()) and request.method == "GET":
                return True
        return False
    

class SingleOrderItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name = 'Manager').exists():
                if request.method in ["GET","POST","PATCH", "DELETE"]:
                    return True
            elif request.user.groups.filter(name = 'Delivery').exists() and (request.method in ["GET","PATCH"]):
                  return True
            elif (request.user.groups.filter(name = 'Customer').exists()) and request.method == "GET":
                return True
        return False

class ManagerGroupPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name = 'Manager').exists():
                if request.method in ["GET","POST"]:
                    return True
        return False
    

class CartItemsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.groups.filter(name = 'Manager').exists():
                if request.method in ["GET"]:
                    return True
            if request.user.groups.filter(name = 'Customer').exists() and (request.method in ["GET","POST","DELETE"]):
                return True
            
        return False