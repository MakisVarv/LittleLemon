from rest_framework import serializers

from restaurant.models import Booking, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="menu_item_description")
    stock = serializers.IntegerField(source="inventory")

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "title",
            "price",
            "stock",
            "description",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
