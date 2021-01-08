from rest_framework import serializers

from ..models.orders import Order
from ..models.products import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at']


class SubmitOrderSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product_id = serializers.IntegerField()
    option_value_ids = serializers.ListField(child=serializers.IntegerField())

