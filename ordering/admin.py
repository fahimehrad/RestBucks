from django.contrib import admin
from ordering.models.products import Product, ProductOption, OptionValue, Option

admin.site.register(Product)
admin.site.register(ProductOption)
admin.site.register(OptionValue)
admin.site.register(Option)
