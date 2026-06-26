from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
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
    path("cart/menu-items/", views.cart, name="cart"),
    path("orders/", views.get_orders, name="orders"),
    path("orders/<int:order_id>/", views.order_details, name="orders"),
    path("menu-items/", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>/", views.SingleMenuItemView.as_view()),
    path("bookings/", views.BookingAPIView.as_view(), name="bookings"),
    path("api-token-auth/", obtain_auth_token),
    path(
        "booking-availability/",
        views.BookingAvailabilityView.as_view(),
        name="booking-availability",
    ),
]
