from django.urls import path, include
from .api import (UserAPI, user_signup_view, tutor_signup_view, login_view)
from knox import views as knox_views

urlpatterns = [
    path('', include('knox.urls')),
    path('parent-signup/', user_signup_view),
    path('tutor-signup/', tutor_signup_view),
    path('login-user/', login_view),
    path('user/', UserAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')
]
