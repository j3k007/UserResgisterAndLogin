from django.urls import path
from .views import (UserRegistration, 
                    UserLogin, 
                    UserProfileView, 
                    UserPasswordChangeView)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='Register'),
    path('login/', UserLogin.as_view(), name='Login'),
    path('profileInfo/', UserProfileView.as_view(), name='UserInfo'),
    path('updatePassword/', UserPasswordChangeView.as_view(), name='ChangePassword'),
    
]