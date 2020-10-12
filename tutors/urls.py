from django.urls import path
from .views import (
    TutorList,
    TutorCreate,
    TutorDetail,
    TuTutorRequestList
)
urlpatterns = [
    path('tutoring_plan_list/', TutorList.as_view(), name='tutoring_plan_list'),
    path('create/', TutorCreate.as_view(), name='tutor_create'),
    path('get/<id>/', TutorDetail.as_view(), name='tutor_detail'),
    path('tutor_request_list/', TuTutorRequestList.as_view(),
         name='tutor_request_for_tutoring plan')
]
