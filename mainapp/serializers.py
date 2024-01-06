from rest_framework import serializers
from django.contrib.auth.models import User
from .models import userDetail,Files
class UserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=30)
    name=serializers.CharField(max_length=50)
    email=serializers.CharField(max_length=50)
    password=serializers.CharField(max_length=20)
    def create(self,validated_data):
        User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['email'],first_name=validated_data['name'])
        del validated_data["password"]
        return userDetail.objects.create(**validated_data),
class LoginuserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=30)
    password=serializers.CharField(max_length=20)
class FileSerializer(serializers.Serializer):
    file=serializers.FileField()
    def create(self,validated_data):
        return Files.objects.create(**validated_data),
class DownloadSerializer(serializers.Serializer):
    public_key=serializers.CharField()
