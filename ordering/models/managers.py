from django.db import models


class SafeDelete(models.Manager):
    # this class is used for safe delete
    # we search for records which their deleted_at is not set to a dateTime
    def get_queryset(self):
        return super(SafeDelete, self).get_queryset().filter(deleted_at=None)


class OrderManager(models.Manager):
    # We use this manager to handle queries easier and not to have complex queries in service layer
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

    def get_order_of_user(self, user_id):
        return self.get_queryset().filter(user_id=user_id).order_by('-created_at').last()
