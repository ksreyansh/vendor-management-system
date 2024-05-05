from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from .serializers import UserSerializer


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    def post(self, request):
        if "email" not in request.data and "password" not in request.data:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        elif "password" not in request.data:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(email=request.data['email'], password=request.data['password'])

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    def post(self, request):
        # Get the token from the request headers
        token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        # Check if the token exists
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Delete the token
        token.delete()

        return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)

