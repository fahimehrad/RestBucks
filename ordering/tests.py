from django.test import TestCase
import factory
from django.db.models import signals
from rest_framework.exceptions import ValidationError

from user.models import User
from .enums.order import OrderStatus
from .models.orders import Order
from .models.products import Option, OptionValue, Product, ProductOption
from .services import orders as order_service
from .services import products as product_service


class RestBucksUnitTests(TestCase):

    def setUp(self):
        """
            setup test database
        """
        self.user = User.objects.create_user('fahimehfathian@gmail.com', '1994-7-26', '12345!@#')

        consume_location = Option.objects.create(title='Consume location')
        self.take_away = OptionValue.objects.create(option=consume_location, value='take away')
        self.in_shop = OptionValue.objects.create(option=consume_location, value='is shop')

        size = Option.objects.create(title='Size')
        self.small = OptionValue.objects.create(option=size, value='small')
        self.medium = OptionValue.objects.create(option=size, value='medium')
        self.large = OptionValue.objects.create(option=size, value='large')

        milk = Option.objects.create(title='Milk')
        self.skim = OptionValue.objects.create(option=milk, value='skim')
        self.semi = OptionValue.objects.create(option=milk, value='semi')
        self.whole = OptionValue.objects.create(option=milk, value='whole')

        self.latte = Product.objects.create(title='Latte', price=19000)
        self.cappuccino = Product.objects.create(title='Cappuccino', price=18000)
        self.tea = Product.objects.create(title='Tea', price=13000)
        self.hot_chocolate = Product.objects.create(title='Hot chocolate', price=17000)

        ProductOption.objects.create(product=self.latte, option=consume_location)
        ProductOption.objects.create(product=self.latte, option=milk)
        ProductOption.objects.create(product=self.cappuccino, option=consume_location)
        ProductOption.objects.create(product=self.cappuccino, option=size)
        ProductOption.objects.create(product=self.tea, option=consume_location)
        ProductOption.objects.create(product=self.hot_chocolate, option=consume_location)
        ProductOption.objects.create(product=self.hot_chocolate, option=size)

    def test_get_All_products(self):
        products = product_service.get_all()
        self.assertEqual(len(products), 4)

    # We use this decorator to mock pre-save signal
    @factory.django.mute_signals(signals.pre_save)
    def test_create_order(self,):
        order_service.create_order(self.user.id, self.tea.id, 1, [self.take_away.id])
        order = Order.objects.all().first()
        self.assertEqual(order.status, OrderStatus.WAITING)

    @factory.django.mute_signals(signals.pre_save)
    def test_not_send_all_options_of_product(self):
        try:
            order_service.create_order(self.user.id, self.cappuccino.id, 1, [self.take_away.id])
        except ValidationError as error:
            self.assertEqual(error.detail['message'], 'You have to specify all option values of product')

    @factory.django.mute_signals(signals.pre_save)
    def test_delete_order(self):
        order_service.create_order(self.user.id, self.tea.id, 1, [self.take_away.id])
        order_service.delete_order(self.user.id)
        order = Order.objects.all()
        self.assertEqual(len(order), 0)

    @factory.django.mute_signals(signals.pre_save)
    def test_get_order_of_user(self):
        order_service.create_order(self.user.id, self.tea.id, 2, [self.take_away.id])
        order_service.create_order(self.user.id, self.cappuccino.id, 1, [self.take_away.id, self.small.id])
        [order, products, total_price] = order_service.get_order(self.user.id)
        self.assertEqual(total_price, 2 * self.tea.price + self.cappuccino.price)
        self.assertEqual(len(products), 2)
        self.assertEqual(order.status, OrderStatus.WAITING)

