from django.contrib import admin
from .models import Dish, Order, Shift, Table

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Order)
class OderAdmin(admin.ModelAdmin):
    list_display = ['id',  'status', 'created_at']


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'number']

