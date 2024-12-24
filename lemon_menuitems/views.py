from rest_framework.permissions import IsAuthenticated
from lemon_menuitems.models import Cart, Category,MenuItem
from lemon_menuitems.serializers import MenuItemSerializer, CartSerializer, CategorySerializer
from rest_framework import generics
from lemon_menuitems.permissions import IsManagerOrNot, IsSingleManagerOrNot, IsCustomerOrNot, IsSingleCustomerOrNot
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrNot]

    

class SingleMenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsSingleManagerOrNot]

    def get_model_or_404(self, menu_item):

        try:
            model = MenuItem.objects.get(title=menu_item)
        except MenuItem.DoesNotExist:
            raise Http404({"detail":"Menu item not found"})
        return model

    def get(self, request, menu_item):
        menu_item = self.get_model_or_404(menu_item)
        serializer = MenuItemSerializer(menu_item,context={"request":request} )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrNot]


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated & IsCustomerOrNot]
    
    def list(self, request, *args, **kwargs):

        cart_items = Cart.objects.filter(user = request.user)
        serializer = CartSerializer(cart_items, many = True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user = self.request.user)


class SingleCartView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsSingleCustomerOrNot]

    def delete(self, request, *args, **kwargs):

        Cart.objects.filter(user = request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

