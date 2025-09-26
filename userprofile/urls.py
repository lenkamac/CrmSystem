from django.urls import path
from .views import userprofile

app_name = 'userprofile'

urlpatterns = [
    path('', userprofile, name='register'),
]
