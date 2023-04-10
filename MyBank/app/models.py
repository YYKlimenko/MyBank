from django.contrib.auth import get_user_model
from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=4, unique=True, primary_key=True)
    description = models.CharField(max_length=250, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=5)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(default='Account', max_length=25)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='accounts')
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=12, decimal_places=5)

    def __str__(self):
        return f'{self.user.username} - {self.count} {self.currency.name}'


class Property(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=25, unique=True, primary_key=True)
    description = models.CharField(max_length=250, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=5)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=25, unique=True, primary_key=True)
    description = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    name = models.CharField(max_length=25, unique=True, primary_key=True)
    # market = models.ForeignKey(to=Market, on_delete=models.CASCADE, related_name='stocks')
    description = models.CharField(max_length=250, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=5, null=True)

    def __str__(self):
        return self.name
