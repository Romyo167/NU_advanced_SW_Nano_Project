# d:\Term-4\Advanced sw\Nan-Project-Phase-1\NU_advanced_SW_Nano_Project\myapp\views.py
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User # Import User model
from django.db import IntegrityError # Import for handling existing user error
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .consumers import ChatConsumer
import logging # Make sure logger is configured in settings.py if you use it

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

class SignupView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny] # Anyone can attempt to sign up

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        # Optional: Add password confirmation check if desired
        # password_confirm = request.data.get("password_confirm")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optional: Add more validation (e.g., password complexity, username format) here

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already taken."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create the user (handles password hashing)
            user = User.objects.create_user(username=username, password=password)
            logger.info(f"User '{username}' created successfully.")
            # Do NOT log the user in automatically after signup
            return Response(
                {"message": "Signup successful. Please log in."},
                status=status.HTTP_201_CREATED # Use 201 Created status
            )
        except IntegrityError: # Should be caught by the filter above, but as a fallback
             return Response(
                {"error": "Username already taken."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error during user creation for '{username}': {e}")
            return Response(
                {"error": "An unexpected error occurred during signup."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"User '{username}' logged in successfully.")
            return Response({"message": "Login successful", "username": user.username}, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Login failed for username '{username}'.")
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             logger.info(f"User '{request.user.username}' logging out.")
             logout(request)
             return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        else:
             return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)

class ActiveRoomsView(APIView):
    def get(self, request):
        active_rooms = ChatConsumer.get_active_rooms()
        return Response(active_rooms)

