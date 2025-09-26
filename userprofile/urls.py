from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('', views.user_account, name='account'),
    path('edit/', views.edit_profile, name='edit-profile'),
    path('register/', views.register, name='register')
]
