from django.contrib import admin
from .models import Category, MenuItem
from .models import Booking

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Booking)
