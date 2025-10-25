from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'net_price', 'description', 'sold_quantity')
    list_filter = ('name',)
    search_fields = ('name',)
    readonly_fields = ('sold_quantity',)  # Make sold_quantity read-only



admin.site.register(Product, ProductAdmin)