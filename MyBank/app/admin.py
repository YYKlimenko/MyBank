from django.contrib import admin

from .models import Currency, Account, Property


admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Property)
