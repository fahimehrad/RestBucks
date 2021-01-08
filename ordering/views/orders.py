from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.orders import Order as OrderModel
from ..serializers.orders import SubmitOrderSerializer, OrderSerializer, ProductSerializer
from ..services import orders as order_service


class OrderView(APIView):
    def put(self, request):
        """
            This API create an order if there is no non-delivered order for user and user can add product to her order
            using this api
            Return Ok if nothing goes wrong
            parameters:
                - name: product_id
                      required: true
                      type: integer

                - name: quantity
                  required: true
                  type: integer

                - name: option_value_ids
                  required: true
                  type: array

        """
        try:
            user = request.user
            serializer = SubmitOrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            order_service.create_or_update_order(user.id, data['product_id'], data['quantity'], data['option_value_ids'])
            return Response(data={'result': 'OK'}, status=status.HTTP_200_OK)

        except ValidationError as error:
            return Response(data={'result': 'OK', 'data': error.detail['message']}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        """
            This API will delete the last not delivered order of user
            Return Ok if nothing goes wrong
            parameters:

        """
        try:
            user = request.user
            order_service.delete_order(user.id)
            return Response(data={"result": "OK"}, status=status.HTTP_200_OK)
        except (ValidationError, NotFound) as error:
            return Response(data={'result': 'OK', 'data': error.detail['message']}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        """
            Return user order with the list of it's product and total price of the order
            parameters:

        """
        try:
            [order, products, total_price] = order_service.get_order(request.user)
            data = OrderSerializer(order).data
            product_serializer = ProductSerializer(products, many=True)
            data["products"] = product_serializer.data
            data["total_price"] = total_price
            return Response(data={"result": "OK", data: data}, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(data={'result': 'OK', 'data': error.detail['message']}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """
            this view is just for testing, and it change the order status so we can see if the signal has been sent
            Return Ok if nothing goes wrong
            ---
            parameters:
                - name: status
                  required: true
                  type: string

                - name: order_id
                  required: true
                  type: integer
        """
        input_status = request.data["status"]
        order_id = request.data["order_id"]
        order = OrderModel.objects.get(id=order_id)
        order.status = input_status
        order.save()
        return Response(data={"result": "OK"}, status=status.HTTP_200_OK)
