from rest_framework import serializers
from lemon_orders.models import Order, OrderItem




class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'


    def create(self, validated_data):
        request = self.context['request']
        is_user_manager = request.user.groups.filter(name = "Manager").exists()
        is_user_delivery_crew = request.user.groups.filter(name = "Delivery crew").exists()
        if is_user_delivery_crew or is_user_manager:
            raise serializers.ValidationError({"Only customers can place orders"})
        return validated_data
    
class OrderItemSerializer(serializers.ModelSerializer):
    pass