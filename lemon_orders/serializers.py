from rest_framework import serializers
from lemon_orders.models import Order, OrderItem
from lemon_menuitems.models import Cart
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','order','menuitem','quantity','unit_price','price']


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total', 'date']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context['request']
  
        if hasattr(instance, 'orderitem_set'):
            menu_items = instance.orderitem_set.all().values()
            if not request.user.groups.filter(name = "Delivery crew").exists():
                data['order items'] = list(menu_items) 
        else:
            data = {"message":"Order successfully placed, Your order will be delivered soon. Thanks!"}
        return data


    def create(self, validated_data):
        request = self.context['request']
        is_user_manager = request.user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = request.user.groups.filter(name = "Delivery crew").exists()

        if is_user_delivery_crew or is_user_manager:
            return Response("You don't have the permission for this",status=status.HTTP_403_FORBIDDEN)
        
        self.throw_field_error(request=request, validated_data=validated_data, message={"fields_error":"You are not allowed to update these fields [user, total, delivery crew].", "order_error": "please click on post without any data to order items of your cart."})
        
        # Get items from cart
        cart_items = Cart.objects.filter(user = request.user)

        if cart_items:
            total = 0
            order = Order.objects.create(user = request.user, date = datetime.now().date(), total = total)
            for cart_item in cart_items:
                total = total + cart_item.price
                OrderItem.objects.create(order = order, menuitem = cart_item.menuitem, quantity = cart_item.quantity, unit_price = cart_item.unit_price, price = cart_item.price)

            order.total = Decimal(total)
            order.save()
            Cart.objects.filter(user = request.user).delete()
        else:
            raise serializers.ValidationError("No item in cart to place an order.")
        return validated_data
    

    def update(self, instance, validated_data):

        request = self.context['request']

        self.throw_field_error(request=request, validated_data=validated_data, message={"fields_error":"You are not allowed to update these fields [user, total, delivery crew].", "order_error": "please click on post without any data to order items of your cart."})
        
        # check if the delivery crew is actually a delivery crew
        if 'delivery_crew' in validated_data:
            delivery_crew = validated_data["delivery_crew"]
            if not delivery_crew.groups.filter(name = "Delivery crew").exists():
                raise serializers.ValidationError({"message":"This user is not a delivery crew."})
        return super().update(instance, validated_data)
    

    def throw_field_error(self,request, validated_data, message):

        is_user_manager = request.user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = request.user.groups.filter(name = "Delivery crew").exists()
            
        if is_user_delivery_crew:
            if 'user' in validated_data or 'delivery_crew' in validated_data or  'total' in validated_data:
                raise serializers.ValidationError({"detail": message["fields_error"]})
        if not is_user_delivery_crew and not is_user_manager:
            delivery_crew = validated_data["delivery_crew"]
            status = validated_data["status"]
            if delivery_crew or status:
                raise serializers.ValidationError({"details": message["order_error"]})
            
        