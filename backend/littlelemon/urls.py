from django.contrib import admin
from django.urls import path, include

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
