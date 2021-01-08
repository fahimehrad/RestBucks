from ordering.models.products import Product


def get_all():
    return Product.objects.all()
