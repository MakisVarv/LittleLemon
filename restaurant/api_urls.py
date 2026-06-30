from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("users/", views.UsersAPIView.as_view(), name="users"),
    path(
        "groups/manager/users/",
        views.ManagerUsersAPIView.as_view(),
        name="manager-users",
    ),
    path(
        "groups/manager/users/<int:user_id>/",
        views.ManagerUsersAPIView.as_view(),
        name="delete-manager",
    ),
    path(
        "groups/delivery-crew/users/",
        views.DeliveryUsersAPIView.as_view(),
        name="delivery-users",
    ),
    path(
        "groups/delivery-crew/users/<int:user_id>/",
        views.DeliveryUsersAPIView.as_view(),
        name="delete-delivery",
    ),
    path("cart/menu-items/", views.CartAPIView.as_view(), name="cart"),
    path("orders/", views.OrderListCreateAPIView.as_view(), name="orders"),
    path(
        "orders/<int:order_id>/",
        views.OrderDetailAPIView.as_view(),
        name="orders-details",
    ),
    path("menu-items/", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>/", views.SingleMenuItemView.as_view()),
    path("categories/", views.CategoryListView.as_view()),
    path("categories/<int:pk>/", views.SingleCategoryView.as_view()),
    path("bookings/", views.BookingAPIView.as_view(), name="bookings"),
    path(
        "booking-availability/",
        views.BookingAvailabilityView.as_view(),
        name="booking-availability",
    ),
]
