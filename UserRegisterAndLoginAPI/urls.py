from django.urls import path, include
from .views import UserRegistration, UserLogin

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='Register'),
    path('login/', UserLogin.as_view(), name='Login')
]