from rest_framework import serializers
from django.contrib.auth.models import User
from restaurant.models import (
    Booking,
    Cart,
    Category,
    MenuItem,
    Order,
    OrderItem,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class MenuItemSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price"]


class MenuItemSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="menu_item_description")
    stock = serializers.IntegerField(source="inventory")
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "title",
            "price",
            "stock",
            "description",
            "category",
            "category_id",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "first_name", "reservation_date", "reservation_slot"]


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSummarySerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "menuitem", "quantity", "unit_price", "price"]


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSummarySerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "menuitem", "quantity", "unit_price", "price"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "delivery_crew",
            "status",
            "total",
            "date",
            "order_items",
        ]
