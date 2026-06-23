from ast import If
from types import NoneType

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from LittleLemonAPI.models import Cart, MenuItem, Order, OrderItem
from LittleLemonAPI.permissions import is_customer, is_delivery_crew, is_manager
from LittleLemonAPI.serializers import (
    CartSerializer,
    MenuItemSerializer,
    OrderSerializer,
    UserSerializer,
)
from rest_framework import status


@api_view()
def home(request):
    return Response({"message": "Hello, world!"})


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
        managers = User.objects.filter(groups__name="Delivery crew")
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


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def menuItems(request):
    if request.method == "GET":
        menu = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        if not is_manager(request.user):
            return Response(
                {"message": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = MenuItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def menuItem(request, id):

    try:
        menuitem = MenuItem.objects.get(id=id)
    except MenuItem.DoesNotExist:
        return Response(
            {"message": "Item not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        serializer = MenuItemSerializer(menuitem)
        return Response(serializer.data)
    if not is_manager(request.user):
        return Response(
            {"message": "You are not authorized"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        menuitem.delete()
        return Response(
            {"message": "Menu item removed successfully"},
            status=status.HTTP_200_OK,
        )
    partial = request.method == "PATCH"
    serializer = MenuItemSerializer(menuitem, data=request.data, partial=partial)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


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
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        if not is_customer(request.user):
            return Response(
                {"message": "Not authorized"}, status=status.HTTP_403_FORBIDDEN
            )
        if is_customer(request.user):
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
