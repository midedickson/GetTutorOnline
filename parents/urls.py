from .views import *
from django.urls.conf import path

urlpatterns = [
    path('add/', ParentCreate.as_view(), name='add_parent'),
    path('get/<pk>/', ParentDetail.as_view(), name='get_parent'),
    path('tutor_request/create/', TutorRequestCreate.as_view(),
         name='create_tutor_request'),
    path('tutor_request/<pk>/', TutorRequestDetail.as_view(),
         name='get_tutor_request'),
]
