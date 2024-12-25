from lemon_menuitems.models import Cart
from lemon_orders.filters import OrderFilter
from lemon_orders.models import Order
from rest_framework.permissions import IsAuthenticated
from lemon_orders.serializers import OrderSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from lemon_orders.paginations import OrderPagination
from lemon_orders.permissions import IsCustomerOrNot, IsSingleManagerOrNot
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated & IsCustomerOrNot]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    pagination_class = OrderPagination
    filterset_class = OrderFilter
    ordering_fields = ['date', 'status','total']

    def get_serializer_context(self):
        return {"request":self.request}


    def filter_orders(self, user):
        is_user_manager = user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = user.groups.filter(name = "Delivery crew").exists()
        if not is_user_delivery_crew and not is_user_manager:
            order = Order.objects.filter(user = user)
        elif is_user_delivery_crew:
            order = Order.objects.filter(delivery_crew = user)
        elif is_user_manager:
            order = Order.objects.all()
        return order

    def list(self, request, *args, **kwargs):

        orders = self.filter_orders(request.user)
        serializer = OrderSerializer(orders, many = True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated & IsSingleManagerOrNot]

    def get_model_or_404(self, pk):
        try:
            model = Order.objects.get(pk = pk)
        except Order.DoesNotExist:
            raise Http404({"detail":"Order not found"})
        return model

    def get(self, request, pk):
        order = self.get_model_or_404(pk)

        is_user_manager = request.user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = request.user.groups.filter(name = "Delivery crew").exists()

        if is_user_delivery_crew and order.delivery_crew != request.user:
            return Response({"You don't have any permission for this"}, status=status.HTTP_403_FORBIDDEN)
        elif not is_user_manager and not is_user_delivery_crew and  order.user != request.user:
            return Response({"You don't have any permission for this"}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order,context={"request":request} )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        menu_item = self.get_model_or_404(pk)
        serializer = OrderSerializer(menu_item,data = request.data, partial = True,  context={"request":request})

        is_user_manager = request.user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = request.user.groups.filter(name = "Delivery crew").exists()

        if not is_user_delivery_crew and not is_user_manager:
            return Response({"You don't have any permission for this"}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"You don't have any permission for this"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        menu_item = self.get_model_or_404(pk)
        serializer = OrderSerializer(menu_item,data = request.data,  context={"request":request})

        is_user_manager = request.user.groups.filter(name = "Manager").exists()

        if not is_user_manager:
            return Response({"You don't have any permission for this"},status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"You don't have any permission for this"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, pk):
        order = self.get_model_or_404(pk)
        if request.user.groups.filter(name = "Manager").exists():
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"You don't have any permission for this"},status=status.HTTP_403_FORBIDDEN)




