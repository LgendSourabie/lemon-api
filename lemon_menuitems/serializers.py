from rest_framework import serializers
from lemon_menuitems.models import Cart, Category,MenuItem
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','slug','title']


class CartSerializer(serializers.ModelSerializer):

    unit_price = serializers.SerializerMethodField(method_name='get_unit_price')
    price = serializers.SerializerMethodField(method_name='calculate_price')

    class Meta:
        model = Cart
        fields = ['id','user','menuitem','quantity','unit_price','price']
        read_only_fields = ['user','unit_price', 'price']
        extra_kwargs = {
            "quantity":{"min_value":1},
        }
    
    def calculate_price(self, cart:Cart):
        return cart.unit_price * cart.quantity
    
    def get_unit_price(self, cart:Cart):
        return cart.menuitem.price

    def validate(self, data):
        menu_item = data['menuitem']
        data['unit_price'] = menu_item.price  
        data['price'] = data['unit_price'] * data['quantity']  
        return data
    
    def create(self, validated_data):

        validated_data['unit_price'] = validated_data['menuitem'].price
        validated_data['price'] = validated_data['unit_price'] * validated_data['quantity']
        current_menu_item = validated_data['menuitem']
        current_user = self.context['request'].user
        cart_items = Cart.objects.filter(user = current_user, menuitem = current_menu_item)

        if len(cart_items) != 0:
            raise serializers.ValidationError("You already have this item in your cart")
        return super().create(validated_data)

    def update(self, instance, validated_data):

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = instance.menuitem.price  
        instance.price = instance.unit_price * instance.quantity
        instance.save()
        return instance
    
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']
        extra_kwargs = {
            "category_id":{"min_value":1},
            "price":{"min_value":0},
             "title":{
                "validators":[
                    UniqueValidator(queryset=MenuItem.objects.all())
                ]
            }
        }


    def validate(self, attrs):

        category_id = attrs.get('category_id','')
        if category_id:
            try:
                Category.objects.get(pk = category_id)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"Category does not exist"})
        return attrs