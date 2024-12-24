from lemon_menuitems.models import Cart
from lemon_orders.filters import OrderFilter
from lemon_orders.models import Order, OrderItem

from lemon_orders.serializers import OrderSerializer, OrderItemSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from lemon_orders.paginations import OrderPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ['date', 'status','total']

    def get_serializer_context(self):
        return {"request":self.request}
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user = request.user)
        return super().create(request, *args, **kwargs)
    

    def filter_orders(self, user):
        is_user_manager = user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = user.groups.filter(name = "Delivery crew").exists()
        if not is_user_delivery_crew and not is_user_manager:
            order = Order.objects.filter(user = user)
        elif is_user_delivery_crew:
            order = Order.objects.filter(delivery_crew = user)
        else:
            order = Order.objects.all()
        return order

    def list(self, request, *args, **kwargs):

        orders = self.filter_orders(request.user)
        serializer = OrderSerializer(orders, many = True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_model_or_404(self, pk):
        try:
            model = Order.objects.get(pk = pk)
        except Order.DoesNotExist:
            raise Http404({"detail":"Order not found"})
        return model

    def get(self, request, pk):
        order_item = self.get_model_or_404(pk)
        serializer = OrderSerializer(order_item,context={"request":request} )
        return Response(serializer.data, status=status.HTTP_200_OK)




