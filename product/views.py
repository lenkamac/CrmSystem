
from django.contrib.auth.mixins import LoginRequiredMixin

from product.models import Product
from django.views.generic import ListView, DetailView


# Create your views here.
class ProductListView(ListView):
    model = Product

    template_name = 'product/products-list.html'
    context_object_name = 'products'
    ordering = ['-id']


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product-detail.html'
    context_object_name = 'product'