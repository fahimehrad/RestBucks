from ordering.enums.order import OrderStatus
from ordering.models.products import Product, OptionValue
from user.models import User
from django.db import models
from .managers import OrderManager, SafeDelete


class Order(models.Model):
    # this is the main model for our orders
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatus.choices)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = OrderManager()

    def __str__(self):
        return self.user.email + self.status

    class Meta:
        db_table = 'restBucks_order'


class OrderProduct(models.Model):
    # This model specifies which product and how many of that exist in the order
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SafeDelete()

    def __str__(self):
        return self.order.status + self.product.title

    class Meta:
        db_table = 'restBucks_orderProduct'


class OrderProductOptionValue(models.Model):
    # This model specifies which values the customer has chosen in her order
    order_product = models.ForeignKey(OrderProduct, related_name='option_values', on_delete=models.CASCADE)
    optionValue = models.ForeignKey(OptionValue, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SafeDelete()

    class Meta:
        db_table = 'restBucks_orderProductOptionValue'
