from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password":{"write_only":True}
        }
    
    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        
        if password != password2:
            return serializers.ValidationError({"Error":"Password does not match. Try Again!"})
        
        if User.objects.filter(email=email).exists():
            return serializers.ValidationError({"Error":"This email already exists. Try another one."})
    
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()
        return account
    