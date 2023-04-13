from django.contrib.auth import get_user_model
from django.db import models

from .protocols import UserProtocol


class AssetCategory(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.CharField(max_length=250, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=5, null=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='assets')

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(default='Account', max_length=25)
    user: UserProtocol = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='accounts')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=12, decimal_places=5)

    def __str__(self):
        return f'{self.user.username} - {self.count} {self.asset.name}'


class Property(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=5)

    def __str__(self):
        return self.name
