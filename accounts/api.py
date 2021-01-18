from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from knox.models import AuthToken
from .serializers import UserSerilizer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import traceback
from parents.models import ParentProfile
from tutors.models import Tutor
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Register API

'''
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerilizer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerilizer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
'''


def validate_signup(email, first_name, last_name, password, password2):
    validation = {}
    import re
    # for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    # function for validating an Email

    def check_email(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email) is not None:
            return True
        else:
            return False

    def check_name(name):
        if re.search("[a-zA-Z]", name) is not None:
            return True
        else:
            return False
    if not check_email(email):
        validation['email'] = 'Please anter a valid Email address!'
    if not check_name(first_name):
        validation['first_name'] = 'Names must contain only alphabets!'
    if not check_name(last_name):
        validation['first_name'] = 'Names must contain only alphabets!'
    if password == '':
        validation['password'] = 'Please set a password!'
    if password != password2:
        validation['confirm_password'] = 'Passwords must match!'
    if len(validation) != 0:
        return validation
    else:
        return None


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_signup_view(request):
    payload = json.loads(request.body)
    try:
        username = payload['username']
        email = payload['email']
        password = payload['password']
        password2 = payload['password2']
        first_name = payload['first_name']
        last_name = payload['last_name']
        try:
            check_username = User.objects.get(username=username)
            if check_username:
                return Response({'message': 'A user with that username already exists. Your username can contain alphabets numbers and characters. Example: steveAde1'}, status=400)
        except User.DoesNotExist:
            pass
        # validation
        try:
            check_email = User.objects.get(email=email)
        except User.DoesNotExist:
            # validate user Email
            valid = validate_signup(
                email, first_name, last_name, password, password2)
            if valid is not None:
                return Response(valid, status=400)
            else:
                pass
        else:
            return Response({
                'message': 'It seems you have previuosly signed up on Get Tutor. Login to continue or Check that you are using the correct email.'
            }, status=400)
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.active = True
        user.save()
        ParentProfile.objects.create(user=user)
        # response = json.dumps([{ 'message': 'Check your email for account activation link. It may take several minutes to arrive'}])
        return Response({
            'token': AuthToken.objects.create(user)[1],
            'message': 'Sign up successful',
        }, status=200)
        # # send emails using sendgrid
        # send_mail(
        #     email_subject,
        #     message,
        #     'clarityadmin@yudimy.com',
        #     [email],
        #     fail_silently=False,
        # )
    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_traceback = traceback.extract_tb(ex_traceback)
        print(ex_type)
        print(ex_value)
        print(ex_traceback)
        return Response({'message': 'Something went wrong. Please try again.'}, status=500)



@api_view(["POST"])
@permission_classes((AllowAny,))
def tutor_signup_view(request):
    payload = json.loads(request.body)
    try:
        username = payload['username']
        email = payload['email']
        password = payload['password']
        password2 = payload['password2']
        first_name = payload['first_name']
        last_name = payload['last_name']
        try:
            check_username = User.objects.get(username=username)
            if check_username:
                return Response({'message': 'A user with that username already exists'}, status=400)
        except User.DoesNotExist:
            pass
        try:
            check_email = User.objects.get(email=email)
        except User.DoesNotExist:
            # validate user Email
            valid = validate_signup(
                email, first_name, last_name, password, password2)
            if valid is not None:
                return Response(valid, status=400)
            else:
                pass
        else:
            return Response({
                'message': 'It seems you have previuosly signed up on Get Tutor. Login to continue or Check that you are using the correct email.'
            }, status=400)
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.active = True
        user.save()
        profile = ParentProfile.objects.create(user=user, is_tutor=True)
        Tutor.objects.create(profile=profile)
        # response = json.dumps([{ 'message': 'Check your email for account activation link. It may take several minutes to arrive'}])
        return Response({
            'token': AuthToken.objects.create(user)[1],
            'message': 'Sign up successful! You can now procceed to your tutor application form. As a bonus, you also have access to a parent dashbaord, where you can hire other tutors too',
        }, status=200)
    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_traceback = traceback.extract_tb(ex_traceback)
        print(ex_type)
        print(ex_value)
        print(ex_traceback)
        return Response({'message': 'Something went wrong. Please try again.'}, status=500)

# Login API



@api_view(["POST"])
def login_view(request):
    payload = json.loads(request.body)
    username = payload["username"]
    password = payload["password"]
    if username is None or password is None or username == '' or password == '':
        return Response({'message': 'Please provide both email/username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'message': 'Have you signed up with us? Try the sign up option or check that you are using the correct login details.'}, status=400)
    if user and not user.is_active:
        return Response({'message': 'Please check that you have verified your account. Kindly check your email for an activation link.'}, status=400)
    token = AuthToken.objects.create(user)[1]
    return Response(
        {
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_tutor': user.parentprofile.is_tutor
            }
        },
        status=200
    )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerilizer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Get User API


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerilizer

    def get_object(self):
        return self.request.user
