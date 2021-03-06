
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('Profile/', Profile.as_view(), name="profile"),
    path('profile-update/<int:pk>', ProfileUpdate.as_view(), name="profile_update")
    
]
