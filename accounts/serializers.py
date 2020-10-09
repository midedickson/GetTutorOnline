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
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

# Register Serializer


class RegisterSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = self.validated_data['email']
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise serializers.ValidationError(
                'This e-mail has already been used by another user'
            )
        else:
            user = User.objects.create_user(
                validated_data['username'], validated_data['email'], password=validated_data['password'])
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            user.is_active = True
            user.save()
            '''
            uidb64 = force_bytes(urlsafe_base64_encode(user.pk))
            link = reverse('activate', kwargs={
                           'uidb64': uidb64, 'token': token_generator.make_token(user)})
            subject = 'Welcome, ' + user.first_name + '!'
            message = 'Thank You for registering with Us.\n For Certain security measures, \
                we are sending you this to verify your email address, Click on the link below to activate your account!\n' + 'https://mingle-market.herokuapp.com' + link
            mail = EmailMessage(
                subject, message, settings.EMAIL_HOST_USER, [email])
            mail.send(fail_silently=False)
            '''
            return user
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
