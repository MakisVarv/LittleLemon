from django.shortcuts import render
from .forms import BookingForm
from .models import MenuItem
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import viewsets
from .serializers import BookingSerializer


# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# Create your views here.
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def reservations(request):
    date = request.GET.get("date", datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize("json", bookings)
    return render(request, "bookings.html", {"bookings": booking_json})


def book(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "book.html", context)


def menu(request):
    menu_data = MenuItem.objects.all()
    main_data = {"menu": menu_data}
    return render(request, "menu.html", {"menu": main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = MenuItem.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, "menu_item.html", {"menu_item": menu_item})


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        date = data["reservation_date"]
        slot = data["reservation_slot"]

        exists = (
            Booking.objects.filter(reservation_date=date)
            .filter(reservation_slot=slot)
            .exists()
        )
        if exists:
            return HttpResponse('{"error": 1}', content_type="application/json")

        Booking.objects.create(
            first_name=data["first_name"],
            reservation_date=date,
            reservation_slot=slot,
        )

    else:
        date = request.GET.get("date", datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize("json", bookings)
    return HttpResponse(booking_json, content_type="application/json")
