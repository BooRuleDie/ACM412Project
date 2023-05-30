from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login, name='login'),
    path('signup/', Signup, name='signup'),
    path('home/', Home, name='home'),
]
