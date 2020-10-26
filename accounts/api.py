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


@csrf_exempt
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
                return Response({'message': 'A user with that username already exists'}, status=400)
        except User.DoesNotExist:
            pass
        try:
            check_email = User.objects.get(email=email)
            # Python program to validate an Email
            import re
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            # for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
            # function for validating an Email

            def check(email):

                # pass the regular expression
                # and the string in search() method
                if(re.search(regex, email)):
                    return True

                else:
                    return False

            # Driver Code
            # Enter the email

            if not check(email):
                return Response({'message': 'Please Enter a valid email'}, status=400)

            if check_email:
                return Response({
                    'message': 'It seems you have previuosly signed up on our Get Tutor. Login to continue or Check that you are using the correct email.'
                }, status=400)
        except User.DoesNotExist:
            pass
        # elif check_email and not check_email.active:
        #     # token_validity_check = check_email.token_time_stamp
        #     # if generate_token.check_token(check_user, token_validity_check):
        #     response = json.dumps(
        #         [{'message': 'Email already registered. Please check your email for activation link'}])
        #     return Response(response, content_type='text/json', status=400)
        if password == password2:
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
            # user.type = User.Types.CLARITYCOUNSELLOR
            # user_token = generate_token.make_token(user)
            # user.token_time_stamp = user_token
            # try:
            # email_subject = 'Activate your account'
            # message = render_to_string('activateclarity.html', {
            #     'user':first_name,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':user_token
            # })

            # # send emails using mailgun
            # # requests.post(
            # #     "https://api.mailgun.net/v3/yudimy.com/messages",
            # #     auth=("api", "7a9aa2a6a626aa7adaab58f2688350e6-913a5827-460c3ac0"),
            # #     data={"from": "Clarity By Yudimy <clarityadmin@yudimy.com>",
            # #         "to": [email],
            # #         "subject": email_subject,
            # #         "text": message})

            # # send emails using sendgrid
            # send_mail(
            #     email_subject,
            #     message,
            #     'clarityadmin@yudimy.com',
            #     [email],
            #     fail_silently=False,
            # )
            # user.save()

            # except BaseException as e:
            #     # ex_type, ex_value, ex_traceback = sys.exc_info()
            #     # ex_traceback = traceback.extract_tb(ex_traceback)
            #     # print(ex_type)
            #     # print(ex_value)
            #     # print(ex_traceback)
            #     response = json.dumps([{'message': 'Error in signing up'}])
            #     return Response(response, content_type='text/json', status=500)
        else:
            return Response({'message': 'Passwords must match'}, status=400)

    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_traceback = traceback.extract_tb(ex_traceback)
        print(ex_type)
        print(ex_value)
        print(ex_traceback)
        return Response({'message': 'Something went wrong. Please try again.'}, status=500)


@csrf_exempt
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
            # Python program to validate an Email
            import re
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            # for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
            # function for validating an Email

            def check(email):

                # pass the regular expression
                # and the string in search() method
                if(re.search(regex, email)):
                    return True

                else:
                    return False

            # Driver Code
            # Enter the email

            if not check(email):
                return Response({'message': 'Please Enter a valid email'}, status=400)

            if check_email:
                return Response({
                    'message': 'It seems you have previuosly signed up on our Get Tutor. Login to continue or Check that you are using the correct email.'
                }, status=400)
        except User.DoesNotExist:
            pass
        # elif check_email and not check_email.active:
        #     # token_validity_check = check_email.token_time_stamp
        #     # if generate_token.check_token(check_user, token_validity_check):
        #     response = json.dumps(
        #         [{'message': 'Email already registered. Please check your email for activation link'}])
        #     return Response(response, content_type='text/json', status=400)
        if password == password2:
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
            # user.type = User.Types.CLARITYCOUNSELLOR
            # user_token = generate_token.make_token(user)
            # user.token_time_stamp = user_token
            # try:
            # email_subject = 'Activate your account'
            # message = render_to_string('activateclarity.html', {
            #     'user':first_name,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':user_token
            # })

            # # send emails using mailgun
            # # requests.post(
            # #     "https://api.mailgun.net/v3/yudimy.com/messages",
            # #     auth=("api", "7a9aa2a6a626aa7adaab58f2688350e6-913a5827-460c3ac0"),
            # #     data={"from": "Clarity By Yudimy <clarityadmin@yudimy.com>",
            # #         "to": [email],
            # #         "subject": email_subject,
            # #         "text": message})

            # # send emails using sendgrid
            # send_mail(
            #     email_subject,
            #     message,
            #     'clarityadmin@yudimy.com',
            #     [email],
            #     fail_silently=False,
            # )
            # user.save()

            # except BaseException as e:
            #     # ex_type, ex_value, ex_traceback = sys.exc_info()
            #     # ex_traceback = traceback.extract_tb(ex_traceback)
            #     # print(ex_type)
            #     # print(ex_value)
            #     # print(ex_traceback)
            #     response = json.dumps([{'message': 'Error in signing up'}])
            #     return Response(response, content_type='text/json', status=500)
        else:
            return Response({'message': 'Passwords must match'}, status=400)

    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_traceback = traceback.extract_tb(ex_traceback)
        print(ex_type)
        print(ex_value)
        print(ex_traceback)
        return Response({'message': 'Something went wrong. Please try again.'}, status=500)

# Login API


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_view(request):
    payload = json.loads(request.body)
    username = payload["username"]
    password = payload["password"]
    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
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
