from django.urls import path
from . import views

app_name = 'lead'

urlpatterns = [
    path('', views.lead, name='lead'),
]