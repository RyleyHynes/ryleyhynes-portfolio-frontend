from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta: model = Profile; fields = ["display_name","role"]
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta: model = User; fields = ["id","username","email","first_name","last_name","profile"]
