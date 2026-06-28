from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_manager(user):
    return user.is_authenticated and user.groups.filter(name="Manager").exists()


def is_delivery_crew(user):
    return user.is_authenticated and user.groups.filter(name="Delivery crew").exists()


def is_customer(user):
    return user.is_authenticated and not is_manager(user) and not is_delivery_crew(user)


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return is_customer(request.user)


class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return is_manager(request.user)
