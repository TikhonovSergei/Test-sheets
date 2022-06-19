from django.contrib import admin
from .models import *

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("number", "number_order", "price_dolars", "price_rubles", "data_deliveries",)