from django.shortcuts import render
from .forms import BookingForm
from datetime import datetime
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Booking
from .serializers import MenuItemSerializer, BookingSerializer, UserSerializer
from rest_framework import viewsets
from .permissions import IsManagerOrReadOnly, is_customer, is_delivery_crew, is_manager
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def manager_users(request):

    if not is_manager(request.user):
        return Response(
            {"message": "You are not authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "GET":
        managers = User.objects.filter(groups__name="Manager")
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        userId = request.data.get("user_id")

        if userId is None:
            return Response(
                {"message": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(id=userId)
            manager_group = Group.objects.get(name="Manager")
            user.groups.add(manager_group)
            return Response(
                {"message": "User added to Manager group"},
                status=status.HTTP_201_CREATED,
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_User_from_Managers(request, user_id):
    if not is_manager(request.user):
        return Response(
            {"message": "You are not authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    manager_group = Group.objects.get(name="Manager")
    if not user.groups.filter(name="Manager").exists():
        return Response(
            {"message": "User not in manager group"},
            status=status.HTTP_404_NOT_FOUND,
        )
    user.groups.remove(manager_group)
    return Response(
        {"message": "User removed from Manager group"},
        status=status.HTTP_200_OK,
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def delivery_users(request):

    if not is_manager(request.user):
        return Response(
            {"message": "You are not authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "GET":
        delivery_crew = User.objects.filter(groups__name="Delivery crew")
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        userId = request.data.get("user_id")

        if userId is None:
            return Response(
                {"message": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(id=userId)
            delivery_group = Group.objects.get(name="Delivery crew")
            user.groups.add(delivery_group)
            return Response(
                {"message": "User added to delivery crew"},
                status=status.HTTP_201_CREATED,
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_User_from_Delivery(request, user_id):
    if not is_manager(request.user):
        return Response(
            {"message": "You are not authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    delivery_group = Group.objects.get(name="Delivery crew")
    if not user.groups.filter(name="Delivery crew").exists():
        return Response(
            {"message": "User not in delivery crew"},
            status=status.HTTP_404_NOT_FOUND,
        )
    user.groups.remove(delivery_group)
    return Response(
        {"message": "User removed from delivery crew"},
        status=status.HTTP_200_OK,
    )


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]


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
