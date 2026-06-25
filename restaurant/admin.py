from django.contrib import admin

# Register your models here.
from .models import MenuItem
from .models import Booking

admin.site.register(MenuItem)
