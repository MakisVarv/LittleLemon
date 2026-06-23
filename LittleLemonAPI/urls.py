from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="api-home"),
    path("groups/manager/users/", views.manager_users, name="manager-users"),
    path(
        "groups/manager/users/<int:user_id>/",
        views.delete_User_from_Managers,
        name="delete-manager",
    ),
    path("groups/delivery-crew/users/", views.delivery_users, name="manager-users"),
    path(
        "groups/delivery-crew/users/<int:user_id>/",
        views.delete_User_from_Delivery,
        name="delete-manager",
    ),
    path("menu-items/", views.menuItems, name="menu"),
    path("menu-items/<int:id>/", views.menuItem, name="menu"),
    path("cart/menu-items/", views.cart, name="cart"),
    path("orders/", views.get_orders, name="orders"),
    path("orders/<int:order_id>/", views.order_details, name="orders"),
]
