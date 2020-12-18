from django.urls import path
from .views import (
    TutorList,
    TutorCreate,
    TutorDetail,
    TuTutorRequestList,
    ExpertiseListView,
    TutoringPlanDetailView,
    GeneralTutoringPlanList,
    CreateTutorPLan,
    TutorsTutorPlanList,
    TutorProfile,
    create_tutor_plan,
    accept_tutor_request,
    reject_tutor_request
)

from parents.views import (ParentDetail)
urlpatterns = [
    path('general_tutoring_plan_list/', GeneralTutoringPlanList.as_view(),
         name='tutoring_plan_list'),
    path('tutor_tutoring_plan_list', TutorsTutorPlanList.as_view()),
    path('tutor_list', TutorList.as_view(), name='tutor_list'),
    path('create/', TutorCreate.as_view(), name='tutor_create'),
    path('profile/', TutorProfile.as_view(), name='update-profile'),
    path('info/', TutorDetail.as_view(), name='tutor_detail'),
    path('create_tutor_plan/', create_tutor_plan),
    path('tutor_request_list/', TuTutorRequestList.as_view(),
         name='tutor_request_for_tutoring plan'),
    path('expertise', ExpertiseListView.as_view(), name='expertise'),
    path('tutor_plan/', TutoringPlanDetailView.as_view(), name='tutor_plan'),
]
