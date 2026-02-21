from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User.objects.create(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        token, created = Token.objects.get_or_create(user=user)
        return {
            'user': UserSerializer(user).data,
            'token': token.key
        }
    

