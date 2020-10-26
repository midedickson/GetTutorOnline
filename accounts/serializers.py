from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.core.mail import EmailMessage
# User Serializer


class UserSerilizer(serializers.ModelSerializer):
    is_tutor = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'is_tutor')

    def get_is_tutor(self, obj):
        return obj.parentprofile.is_tutor


# Login Serializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        elif user and not user.is_active:
            raise serializers.ValidationError(
                'Please Check Your email inbox to activate your account!')
        raise serializers.ValidationError('Incorect Username or Password!')
