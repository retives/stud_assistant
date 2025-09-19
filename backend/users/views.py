from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.conntrib.auth.models import User
from .serializers import UserSerializer
# Create your views here.
class SignUp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_name = request.data.get('username')
        user_email= request.data.get('email')
        user_password = request.data.get('password')
        user_repeat_password = request.data.get('repeat_password')

        if user_password != user_repeat_password:
            return Response({"error": "Passwords do not match"}, status=400)
        if User.objects.filter(username = user_name).exists():
            return Response({"error": "Username already exists"}, status=400)
        user = User.objects.create(username = user_name, email = user_email, password = user_password)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201)

class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Implement login logic here
        ...