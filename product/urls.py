from django.urls import path
from product.views import *
from . import views

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]