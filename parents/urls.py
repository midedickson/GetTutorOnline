from .views import (
    ParentCreate,
    ParentDetail,
    create_tutor_request,
    TutorRequestDetail,
    ParentTutorRequestList,
    cancel_after24hrs,
    get_tutor_request_list
)
from django.urls.conf import path

urlpatterns = [
    path('add/', ParentCreate.as_view(), name='add_parent'),
    path('get/', ParentDetail.as_view(), name='get_parent'),
    path('create-tutor-request/', create_tutor_request,
         name='create_tutor_request'),
    path('tutor_request/<pk>/', TutorRequestDetail.as_view(),
         name='get_tutor_request'),
    path('tutor-requests/', ParentTutorRequestList.as_view(),
         name='parent_tutor_requests'),
#     path('24_hours_cancel_request/<pk>/',
#          cancel_after24hrs, name='24_hours_cancel_request'),
#     path('get_tutor_request_list', get_tutor_request_list,
#          name='get_tutor_request_list')
]
