from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    # These are the statuses that an order can have
    WAITING = 'WAITING', _('WAITING')
    PREPARATION = 'PREPARATION', _('PREPARATION')
    READY = 'READY', _('READY')
    DELIVERED = 'DELIVERED', _('DELIVERED')
