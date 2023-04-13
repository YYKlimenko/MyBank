from django.contrib import admin

from .models import Account, Asset, AssetCategory, Property

admin.site.register(Asset)
admin.site.register(AssetCategory)
admin.site.register(Account)
admin.site.register(Property)

