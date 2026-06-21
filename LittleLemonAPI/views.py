from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer, UserSerializer
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from .permissions import IsManagerOrReadOnly, IsManager
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework import status


class CategoriesView(generics.ListCreateAPIView):
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


@api_view()
def home(request):
    return Response({"message": "Little Lemon API"})


# @api_view()
# def menu_items(request):
#     items = MenuItem.objects.all()
#     serialized_items = MenuItemSerializer(items, many=True)
#     return Response(serialized_items.data)


# @api_view()
# def categories(request):
#     items = Category.objects.all()
#     serialized_items = CategorySerializer(items, many=True)
#     return Response(serialized_items.data)


# @api_view()
# def single_item(request, id):
#     item = MenuItem.objects.get(pk=id)
#     serialized_item = MenuItemSerializer(item)
#     return Response(serialized_item.data)
