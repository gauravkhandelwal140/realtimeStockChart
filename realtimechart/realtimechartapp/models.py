from django.db import models

# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    dateTime = models.BigIntegerField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()