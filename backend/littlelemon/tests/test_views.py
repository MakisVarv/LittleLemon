from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from backend.restaurant.models import MenuItem
from backend.restaurant.serializers import MenuItemSerializer


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

        MenuItem.objects.create(
            title="IceCream",
            price=80,
            inventory=100,
            menu_item_description="Cold dessert",
        )
        MenuItem.objects.create(
            title="Pasta",
            price=12,
            inventory=50,
            menu_item_description="Italian pasta",
        )

    def test_getall(self):
        response = self.client.get("/api/menu-items/")
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)  # type: ignore
