from django.db import models
from .managers import SafeDelete


class Product(models.Model):
    # This model is the main model for our product
    title = models.CharField(max_length=20)
    price = models.IntegerField(blank=True, null=True)
    is_customizable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SafeDelete()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'restBucks_product'


class Option(models.Model):
    # this model specifies different options that products can have
    # two products may have same options so we made it as a separated model
    title = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SafeDelete()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'restBucks_option'


class OptionValue(models.Model):
    # This model specifies the values which an option can have
    value = models.CharField(max_length=20)
    option = models.ForeignKey(Option, related_name='option_value', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SafeDelete()

    def __str__(self):
        return self.option.title + " " + self.value

    class Meta:
        db_table = 'restBucks_optionValue'


class ProductOption(models.Model):
    # This model Specifies which options a product can have
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_options', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SafeDelete()

    def __str__(self):
        return self.product.title + " " + self.option.title

    class Meta:
        db_table = 'restBucks_productOption'