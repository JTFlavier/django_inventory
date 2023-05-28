from rest_framework import serializers
from .models import Order, Customer, Item


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'items', 'customer']