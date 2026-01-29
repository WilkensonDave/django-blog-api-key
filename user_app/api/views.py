from user_app.api import serializers
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

@api_view(["POST",])
def register_view(request):
    if request.method == "POST":
        serializer = serializers.RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data["username"] = account.username
            data["email"] = account.email
            
            token = Token.objects.get(user=account).key
            data["response"] = "You have been successfully registered"
            data["token"] = token
            
        else:
            data = serializer.errors
    
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(["POST",])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)