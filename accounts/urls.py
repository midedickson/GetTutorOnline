from django.urls import path, include
from .api import (UserAPI, user_signup_view, login_view, tutor_signup_view)
from knox import views as knox_views

urlpatterns = [
    path('', include('knox.urls')),
    path('parent_signup', user_signup_view),
    path('tutor_signup', tutor_signup_view),
    path('login', login_view),
    path('user/', UserAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')
]
