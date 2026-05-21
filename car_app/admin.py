from django.contrib import admin
from .models import Manufacturer, Car

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name', 'year', 'car_type', 'hp', 'price')
    list_filter = ('manufacturer', 'car_type', 'engine_type')
    search_fields = ('model_name',)

# Register your models here.
