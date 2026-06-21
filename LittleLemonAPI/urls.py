from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="api-home"),
    path("menu-items/", views.MenuItemsView.as_view(), name="menu-items"),
    path("menu-items/<int:pk>/", views.SingleMenuItemView.as_view(), name="menu-item"),
    path("category", views.CategoriesView.as_view(), name="category"),
    path(
        "groups/manager/users/", views.ManagerUsersView.as_view(), name="manager-users"
    ),
    path(
        "groups/manager/users/<int:user_id>/",
        views.ManagerUserDetailView.as_view(),
        name="manager-user-detail",
    ),
    path(
        "groups/delivery-crew/users/",
        views.DeliveryCrewUsersView.as_view(),
        name="delivery-crew-users",
    ),
    path(
        "groups/delivery-crew/users/<int:user_id>/",
        views.DeliveryCrewUserDetailView.as_view(),
        name="delivery-crew-user-detail",
    ),
]
