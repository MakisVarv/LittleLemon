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
from .models import Cart, MenuItem, Booking, Order, OrderItem
from .serializers import (
    CartSerializer,
    MenuItemSerializer,
    BookingSerializer,
    OrderSerializer,
    UserSerializer,
)
from rest_framework import viewsets
from .permissions import IsManagerOrReadOnly, is_customer, is_delivery_crew, is_manager
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework.pagination import PageNumberPagination


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


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def cart(request):
    if not is_customer(request.user):
        return Response(
            {"message": "only customers have cart"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "GET":
        cartItems = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cartItems, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        menuitem = request.data.get("menuitem")
        qty = request.data.get("quantity")
        if menuitem is None or qty is None:
            return Response(
                {"message": "invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            return Response(
                {"message": "Quantity must be a number"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if qty <= 0:
            return Response(
                {"message": "invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            menuitem = MenuItem.objects.get(id=menuitem)
        except MenuItem.DoesNotExist:
            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        existing_cart_item = Cart.objects.filter(
            user=request.user, menuitem=menuitem
        ).first()
        if existing_cart_item is None:
            unit_price = menuitem.price
            price = unit_price * qty
            cart_item = Cart.objects.create(
                user=request.user,
                menuitem=menuitem,
                quantity=qty,
                unit_price=unit_price,
                price=price,
            )
            serializer = CartSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            unit_price = menuitem.price
            existing_cart_item.quantity += qty
            price = unit_price * existing_cart_item.quantity
            existing_cart_item.unit_price = unit_price
            existing_cart_item.price = price
            existing_cart_item.save()
            serializer = CartSerializer(existing_cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        Cart.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Cart cleared successfully"},
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_orders(request):
    if request.method == "GET":
        if is_manager(request.user):
            orders = Order.objects.all()
        elif is_delivery_crew(request.user):
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)
        status_filter = request.query_params.get("status")
        if status_filter:
            if status_filter not in [0, 1, True, False, "0", "1"]:
                return Response(
                    {"message": "Invalid query"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            status_filter = status_filter in [1, True, "1"]
            orders = orders.filter(status=status_filter)
        ordering = request.query_params.get("ordering")
        if ordering:
            if ordering not in ["date", "-date", "total", "-total"]:
                return Response(
                    {"message": "Invalid query"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            orders = orders.order_by(ordering)
        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == "POST":
        if not is_customer(request.user):
            return Response(
                {"message": "Not authorized"}, status=status.HTTP_403_FORBIDDEN
            )
        cartItems = Cart.objects.filter(user=request.user)
        if not cartItems.exists():
            return Response(
                {"message": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        total = 0
        for i in cartItems:
            total += i.price
        order = Order.objects.create(
            user=request.user,
            delivery_crew=None,
            status=False,
            total=total,
        )
        for i in cartItems:
            orderitem = OrderItem.objects.create(
                order=order,
                menuitem=i.menuitem,
                quantity=i.quantity,
                unit_price=i.unit_price,
                price=i.price,
            )
        cartItems.delete()
        return Response(
            {"message": "Order created successfully"},
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"message": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        if is_manager(request.user):
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif is_delivery_crew(request.user) and order.delivery_crew == request.user:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif is_customer(request.user) and order.user == request.user:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )
    if is_manager(request.user):
        if request.method == "DELETE":
            order.delete()
            return Response(
                {"message": "Order deleted successfully"},
                status=status.HTTP_200_OK,
            )
        order_status = request.data.get("status")
        delivery_id = request.data.get("delivery_crew")
        if order_status is None and delivery_id is None:
            return Response(
                {
                    "message": "Manager is allowed to change only status or delivery crew"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if order_status is not None:
            valid_statuses = [0, 1, True, False, "0", "1"]
            if order_status not in valid_statuses:
                return Response(
                    {"message": "Not valid status"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            order.status = order_status in [1, True, "1"]
        if delivery_id is not None:
            try:
                delivery_user = User.objects.get(id=delivery_id)
            except User.DoesNotExist:
                return Response(
                    {"message": "Delivery User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not delivery_user.groups.filter(name="Delivery crew").exists():
                return Response(
                    {"message": "User is not a delivery crew"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            order.delivery_crew = delivery_user
        order.save()
        return Response(
            {"message": "Order updated successfully"},
            status=status.HTTP_200_OK,
        )
    elif is_delivery_crew(request.user):
        if request.method != "PATCH" or order.delivery_crew != request.user:
            return Response(
                {"message": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            allowed_fields = {"status"}

            if not set(request.data.keys()).issubset(allowed_fields):
                return Response(
                    {"message": "Delivery crew can update only status"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            order_status = request.data.get("status")
            if order_status is None:
                return Response(
                    {"message": "Status is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            valid_statuses = [0, 1, True, False, "0", "1"]
            if order_status not in valid_statuses:
                return Response(
                    {"message": "Not valid status"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            order.status = order_status in [1, True, "1"]
            order.save()
            return Response(
                {"message": "Order status was updated successfully"},
                status=status.HTTP_200_OK,
            )
    else:
        return Response(
            {"message": "You are not authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )
