from django.db import models
from django.conf import settings


class Order(models.Model):
    id=models.AutoField(primary_key = True)
    order_date=models.DateTimeField()
    status=models.CharField(max_length = 15)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
