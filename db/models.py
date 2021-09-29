import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


# User model
class User(models.Model):
    name = models.CharField(max_length=50)
    telegram_id = models.BigIntegerField()
    milma_id = models.IntegerField()
    phone = models.CharField(max_length=255)
    pword = models.CharField(max_length=5)

    def __str__(self):
        return self.name


# bill model
class DailyBill(models.Model):
    milma_id = models.IntegerField()
    Qty = models.FloatField()
    Fat = models.FloatField()
    Clr = models.FloatField()
    Snf = models.FloatField()
    Rate = models.FloatField()
    Amount = models.FloatField()
    AM_Pm = models.CharField(max_length=1)
    Date = models.DateField()

    def __str__(self):
        return self.milma_id
