from rest_framework import serializers

from ..models.products import Product, ProductOption, OptionValue, Option


class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = ['id', 'value']


class OptionSerializer(serializers.ModelSerializer):
    option_value = OptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = Option
        fields = ['id', 'title', 'option_value']


class ProductOptionSerializer(serializers.ModelSerializer):
    option = OptionSerializer()

    class Meta:
        model = ProductOption
        fields = ['option']


class ProductListSerializer(serializers.ModelSerializer):
    product_options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id',
                  'title',
                  'price',
                  'product_options']
