from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, Category, MenuItem, Order, OrderItem
from .serializers import (
    CartSerializer,
    CategorySerializer,
    MenuItemSerializer,
    UserSerializer,
    OrderSerializer,
)

from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from .permissions import IsCustomer, IsManagerOrReadOnly, IsManager
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CategoriesView(generics.ListCreateAPIView):
    permission_classes = [IsManagerOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        category = self.request.GET.get("category")

        if category:
            queryset = queryset.filter(category__title=category)

        return queryset

    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["price", "inventory", "title"]
    search_fields = ["title", "menu_item_description"]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManagerOrReadOnly]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class ManagerUsersView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        managers = User.objects.filter(groups__name="Manager")
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            manager_group = Group.objects.get(name="Manager")
            manager_group.user_set.add(user)
            return Response(
                {"message": "User added to Manager group"},
                status=status.HTTP_201_CREATED,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ManagerUserDetailView(APIView):
    permission_classes = [IsManager]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            manager_group = Group.objects.get(name="Manager")
            manager_group.user_set.remove(user)
            return Response(
                {"message": "User removed from Manager group"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeliveryCrewUsersView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        delivery_crew = User.objects.filter(groups__name="Delivery crew")
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            delivery_group = Group.objects.get(name="Delivery crew")
            delivery_group.user_set.add(user)
            return Response(
                {"message": "User added to Delivery crew group"},
                status=status.HTTP_201_CREATED,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeliveryCrewUserDetailView(APIView):
    permission_classes = [IsManager]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            delivery_group = Group.objects.get(name="Delivery crew")
            delivery_group.user_set.remove(user)
            return Response(
                {"message": "User removed from Delivery crew group"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CartView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        menuitem_id = request.data.get("menuitem")
        quantity = request.data.get("quantity")

        try:
            quantity = int(quantity)
            if quantity < 1:
                return Response(
                    {"error": "Quantity must be at least 1"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            menuitem = MenuItem.objects.get(pk=menuitem_id)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_item, created = Cart.objects.update_or_create(
            user=request.user,
            menuitem=menuitem,
            defaults={
                "quantity": quantity,
                "unit_price": menuitem.price,
                "price": menuitem.price * quantity,
            },
        )

        serializer = CartSerializer(cart_item)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Cart cleared"},
            status=status.HTTP_200_OK,
        )


class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.groups.filter(name="Manager").exists():
            orders = Order.objects.all()
        elif request.user.groups.filter(name="Delivery crew").exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)
        ordering = request.GET.get("ordering")

        if ordering in ["date", "-date", "total", "-total", "status", "-status"]:
            orders = orders.order_by(ordering)
        status_filter = request.GET.get("status")

        if status_filter is not None:
            if status_filter in ["0", "false", "False"]:
                orders = orders.filter(status=False)
            elif status_filter in ["1", "true", "True"]:
                orders = orders.filter(status=True)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        if (
            request.user.groups.filter(name="Manager").exists()
            or request.user.groups.filter(name="Delivery crew").exists()
        ):
            return Response(
                {"error": "Only customers can create orders"},
                status=status.HTTP_403_FORBIDDEN,
            )
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = sum(item.price for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            total=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price,
            )

        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_manager = request.user.groups.filter(name="Manager").exists()
        is_delivery = request.user.groups.filter(name="Delivery crew").exists()

        if is_delivery and not is_manager:
            if order.delivery_crew != request.user:
                return Response(
                    {"error": "This order is not assigned to you"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            status_value = request.data.get("status")

            if status_value is None:
                return Response(
                    {"error": "Status field is required for delivery crew updates"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            order.status = status_value
            order.save()

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if not is_manager:
            return Response(
                {"error": "Only managers or assigned delivery crew can update orders"},
                status=status.HTTP_403_FORBIDDEN,
            )

        delivery_crew_id = request.data.get("delivery_crew")
        status_value = request.data.get("status")

        if delivery_crew_id is not None:
            try:
                delivery_user = User.objects.get(
                    id=delivery_crew_id,
                    groups__name="Delivery crew",
                )
                order.delivery_crew = delivery_user
            except User.DoesNotExist:
                return Response(
                    {"error": "Delivery crew user not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        if status_value is not None:
            order.status = status_value

        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_manager = request.user.groups.filter(name="Manager").exists()
        if not is_manager:
            return Response(
                {"error": "Only managers can delete orders"},
                status=status.HTTP_403_FORBIDDEN,
            )
        order.delete()
        return Response(
            {"message": "Order deleted"},
            status=status.HTTP_200_OK,
        )


@api_view()
def home(request):
    return Response({"message": "Little Lemon API"})
