from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .authentication_backends import EmailAuthBackend
from .models import post, Like

# user register serializer
class RegisterSerializer(serializers.Serializer): 
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()  
    email = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):   # validate data by email if email exists, throw error.
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email alredy Exists!")
        return data
    
    def create(self, validated_data):   # create user with below fields
        user = User.objects.create(username= validated_data['username'], 
                                first_name=validated_data['first_name'],
                                last_name=validated_data['last_name'],
                                email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

# user login serializer 
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):   # validate data
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Account not Found!")
        return data
    
    def get_jwt_token(self, data):    # get Jwt token
        user =  authenticate(email=data['email'], password=data['password'])
        
        if not user:
            return {"message": "invalid credentials", "data": {}}
        
        refresh = RefreshToken.for_user(user)
        return {"message": "Login Success.", "data": {'token':{'refresh': str(refresh),'access': str(refresh.access_token),}}}
    
 
# user post serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        exclude = ['created_at', 'updated_at']   


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'