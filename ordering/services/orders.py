from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound

from ordering.models.orders import OrderProduct, OrderProductOptionValue
from ordering.models.products import OptionValue, ProductOption, Product
from user.models import User
from ..models.orders import Order
from ..enums.order import OrderStatus


def create_or_update_order(user_id, product_id, quantity, option_values_ids):
    order = _get_or_create_user_order(user_id)
    _validate_order_status(order)
    _validate_all_options_mentioned(product_id, option_values_ids)
    order_product, _ = OrderProduct.objects.get_or_create(order=order, product_id=product_id)
    order_product.quantity = quantity
    order_product.save()

    for option_value_id in option_values_ids:
        order_product_option_value, _ = OrderProductOptionValue.objects.get_or_create(order_product_id=order_product.id)
        order_product_option_value.optionValue_id = option_value_id
        order_product_option_value.save()


def delete_order(user_id):
    order = Order.objects.get_order_of_user(user_id)
    if order is None:
        raise NotFound({'message': 'order not found'})
    elif order.status != OrderStatus.DELIVERED:
        order.deleted_at = timezone.now()
        order.save()
    else:
        raise ValidationError({'message': 'You can not delete delivered order'})


def get_order(user_id):
    order = Order.objects.get_order_of_user(user_id)
    order_products = OrderProduct.objects.filter(order=order)
    products = Product.objects.filter(id__in=order_products.values_list('product_id', flat=True))
    total_price = _calculate_total_price(order_products)
    return [order, products, total_price]


def _calculate_total_price(order_products):
    products = map(lambda x: [x.product, x.quantity], order_products)
    total_price = 0
    for item in products:
        [product, quantity] = item
        total_price += product.price * quantity
    return total_price


def _get_or_create_user_order(user_id):
    orders = Order.objects.filter(user_id=user_id).exclude(status=OrderStatus.DELIVERED)
    if len(orders) == 0:
        order = Order.objects.create(user_id=user_id, status=OrderStatus.WAITING)
    else:
        order = orders.order_by('-created_at').last()
    return order


def _validate_all_options_mentioned(product_id, option_values_ids):
    product_options_ids = ProductOption.objects.filter(product_id=product_id).values_list('option_id', flat=True)
    input_option_ids = OptionValue.objects.filter(pk__in=option_values_ids).values_list('option_id', flat=True)
    if sorted(product_options_ids) != sorted(input_option_ids):
        raise ValidationError({'message': 'You have to specify all option values of product'})


def _validate_order_status(order):
    if order.status != OrderStatus.WAITING:
        raise ValidationError({'message': 'You can only update orders with waiting status'})
