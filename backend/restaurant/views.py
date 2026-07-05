from .forms import BookingForm
from datetime import datetime
from django.core import serializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Category, MenuItem, Booking, Order, OrderItem
from .serializers import (
    CartSerializer,
    CategorySerializer,
    MenuItemSerializer,
    BookingSerializer,
    OrderSerializer,
    UserSerializer,
)

from .permissions import (
    IsCustomer,
    IsManager,
    IsManagerOrReadOnly,
    is_customer,
    is_delivery_crew,
    is_manager,
)
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UsersAPIView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class DeliveryUsersAPIView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        delivery_crew = User.objects.filter(groups__name="Delivery crew")
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data)

    def post(self, request):
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

    def delete(self, request, user_id):
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


class ManagerUsersAPIView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        managers = User.objects.filter(groups__name="Manager")
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    def post(self, request):
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

    def delete(self, request, user_id):
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


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrReadOnly]


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrReadOnly]


class BookingAvailabilityView(APIView):
    def get(self, request):
        date = request.query_params.get("date", datetime.today().date())

        all_slots = list(range(12, 22))

        booked_slots = Booking.objects.filter(reservation_date=date).values_list(
            "reservation_slot", flat=True
        )

        available_slots = [slot for slot in all_slots if slot not in booked_slots]

        return Response(
            {
                "date": str(date),
                "available_slots": available_slots,
            },
            status=status.HTTP_200_OK,
        )


class BookingAPIView(APIView):
    def get(self, request):
        if not is_manager(request.user):
            return Response(
                {"message": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        date = request.query_params.get("date", datetime.today().date())
        bookings = Booking.objects.filter(reservation_date=date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        date = serializer.validated_data["reservation_date"]  # type: ignore
        slot = serializer.validated_data["reservation_slot"]  # type: ignore

        exists = Booking.objects.filter(
            reservation_date=date,
            reservation_slot=slot,
        ).exists()

        if exists:
            return Response(
                {"reservation_slot": ["This slot is already booked for this date."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartAPIView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        cartItems = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cartItems, many=True)
        return Response(serializer.data)

    def post(self, request):
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
            existing_cart_item.unit_price = unit_price  # type: ignore
            existing_cart_item.price = price  # type: ignore
            existing_cart_item.save()
            serializer = CartSerializer(existing_cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Cart cleared successfully"},
            status=status.HTTP_200_OK,
        )


class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

    def post(self, request):
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
            OrderItem.objects.create(
                order=order,
                menuitem=i.menuitem,
                quantity=i.quantity,
                unit_price=i.unit_price,
                price=i.price,
            )
        cartItems.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
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

    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if not is_manager(request.user):
            return Response(
                {"message": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )
        order.delete()
        return Response(
            {"message": "Order deleted successfully"},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if is_manager(request.user):
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
            if order.delivery_crew != request.user:
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

        return Response(
            {"message": "You are not authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )


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
