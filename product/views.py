from django.db.models import Q
from django.shortcuts import render
from product.models import Product
from django.views.generic import ListView


# Create your views here.
class ProductListView(ListView):
    model = Product

    template_name = 'product/products-list.html'
    context_object_name = 'products'
    ordering = ['-id']


