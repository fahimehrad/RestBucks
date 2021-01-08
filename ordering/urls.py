from django.urls import path

from ordering.views.products import ProductList
from .views.orders import OrderView

urlpatterns = [
    path('product', ProductList.as_view(), name='product'),
    path('order', OrderView.as_view(), name='order')
]
