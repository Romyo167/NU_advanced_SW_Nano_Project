# d:\Term-4\Advanced sw\Nan-Project-Phase-1\NU_advanced_SW_Nano_Project\myapp\urls.py
from django.urls import path
# Import the new SignupView
from .views import home, ActiveRoomsView, LoginView, LogoutView, SignupView

urlpatterns = [
    path('', home, name='home'),
    # Authentication endpoints
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/signup/', SignupView.as_view(), name='api_signup'), # Add signup URL

    path('api/rooms/', ActiveRoomsView.as_view(), name='active_rooms_list'),
]
