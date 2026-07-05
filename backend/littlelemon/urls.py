from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("restaurant.urls")),
    # Auth routes
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
]
