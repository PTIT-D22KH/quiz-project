from django.urls import path
from . import views
from .models import *
import json
urlpatterns = [
    path('',views.home,name='home'),
    path('welcome/',views.welcome,name='welcome'),
]
