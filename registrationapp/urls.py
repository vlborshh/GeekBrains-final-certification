
from django.urls import path
from . import views

app_name = 'registrationapp'

urlpatterns = [
    path('registr/', views.registration, name='registr')
]