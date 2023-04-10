from django.contrib import admin

from .models import Currency, Account, Property, Stock

admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Property)
admin.site.register(Stock)
