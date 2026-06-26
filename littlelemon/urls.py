from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant import views

router = DefaultRouter()
router.register(r"tables", views.BookingViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    # HTML/template routes
    path("", include("restaurant.urls")),
    # API routes
    path("api/", include("restaurant.api_urls")),
    # Auth routes
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
]
