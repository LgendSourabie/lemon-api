from rest_framework import serializers
from lemon_menuitems.models import Cart, Category,MenuItem





class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','slug','title']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id','user','menuitem','quantity','unit_price','price']


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category']