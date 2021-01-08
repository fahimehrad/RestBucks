from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.products import ProductListSerializer
from ..services import products as product_service


class ProductList(APIView):
    def get(self, request):
        """
            Return all products with options and values of each option
            parameters:

        """
        products = product_service.get_all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
