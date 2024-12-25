from rest_framework.permissions import IsAuthenticated
from lemon_menuitems.models import Cart, Category,MenuItem
from lemon_menuitems.serializers import MenuItemSerializer, CartSerializer, CategorySerializer
from rest_framework import generics
from lemon_menuitems.permissions import IsManagerOrNot, IsSingleManagerOrNot, IsCustomerOrNot
from django.http import Http404
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from lemon_menuitems.paginations import MenuItemPagination
from lemon_menuitems.filters import MenuItemFilter
from rest_framework.response import Response
# Create your views here.


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = MenuItemFilter
    pagination_class = MenuItemPagination
    search_fields = ['title','category__title']
    ordering_fields = ['price']
    permission_classes = [IsManagerOrNot]


    def post(self, request, *args, **kwargs):

        serializer = MenuItemSerializer(data = request.data)

        is_user_manager = request.user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = request.user.groups.filter(name = "Delivery crew").exists()

        if is_user_delivery_crew or is_user_manager:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
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
    
    def delete(self, request, menu_item):
        is_user_manager = request.user.groups.filter(name = "Manager").exists()

        if is_user_manager:
            menu_item = self.get_model_or_404(menu_item)
            menu_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"You don't have any permission for this"}, status=status.HTTP_403_FORBIDDEN)
        

    def put(self, request,menu_item):

        is_user_manager = request.user.groups.filter(name = "Manager").exists()
        menu_item = self.get_model_or_404(menu_item)
        serializer = MenuItemSerializer(menu_item,data = request.data)

        if is_user_manager:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"You don't have any permission for this"}, status=status.HTTP_403_FORBIDDEN)


    def patch(self, request,menu_item):

        is_user_manager = request.user.groups.filter(name = "Manager").exists()

        menu_item = self.get_model_or_404(menu_item)
        serializer = MenuItemSerializer(menu_item,data = request.data, partial = True)

        if is_user_manager:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"You don't have any permission for this"}, status=status.HTTP_403_FORBIDDEN)



class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrNot]


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
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

    def delete(self, request, *args, **kwargs):

        Cart.objects.filter(user = request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
