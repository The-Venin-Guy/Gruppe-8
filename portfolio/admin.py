from django.contrib import admin
from .models import Asset, Stock, CashAccount

admin.site.register(Asset)
admin.site.register(Stock)
admin.site.register(CashAccount)