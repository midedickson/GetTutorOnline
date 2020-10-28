from rest_framework.pagination import PageNumberPagination
import math
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from parents.models import ParentProfile, TutorRequest
from .models import Tutor, Expertise, TutoringPlan
from .serializers import TutorSerializer, TutoringPlanSerializer, ExpertiseSerializer
from .permissions import (
    IsOwnerOrReadOnly,
    IsTutorOrReadOnly,
    IsTutorOwnerOrReadOnly,
    IsTutor,
    IsRequestedTutor

)
from parents.serializers import TutorRequestSerializer, ParentSerializer
import json
import sys
import traceback


@api_view(["GET"])
@permission_classes([IsRequestedTutor, ])
def accept_tutor_request(request, pk):
    user = request.user
    profile = ParentProfile.objects.get(user=user)
    tutor = Tutor.objects.get(profile=profile)
    try:
        tutor_request = TutorRequest.objects.get(id=pk)
        tutor_request.isAccepted = True
        tutor_request.save()
        return Response({'message': 'Well Done, You have succefully accepted this request, your will be connected with the Parent as soon as the payments have been completed'})
    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_traceback = traceback.extract_tb(ex_traceback)
        print(ex_type)
        print(ex_value)
        print(ex_traceback)
        return Response({'message': 'It\'s not you, it\'s us. Please try again.'}, status=500)


@api_view(["GET"])
@permission_classes([IsRequestedTutor, ])
def reject_tutor_request(request, pk):
    user = request.user
    profile = ParentProfile.objects.get(user=user)
    tutor = Tutor.objects.get(profile=profile)
    try:
        tutor_request = TutorRequest.objects.get(id=pk)
        tutor_request.isRejected = True
        tutor_request.save()
        return Response({'message': 'You have rejected this request, this will be communicated to the Parent!'})
    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_traceback = traceback.extract_tb(ex_traceback)
        print(ex_type)
        print(ex_value)
        print(ex_traceback)
        return Response({'message': 'It\'s not you, it\'s us. Please try again.'}, status=500)


def is_valid_queryparam(param):
    return param != '' and param is not None


def tutor_filter(request):
    tutor_qs = Tutor.objects.all()
    # Parameters to be sent to the backend
    name_contains_query = request.GET.get('name_contains')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    expertise = request.GET.get('expertise')
    location = request.GET.get('location')
    grade = request.GET.get('grade')

    if is_valid_queryparam(min_rate):
        tutor_qs = tutor_qs.filter(tutorplan__rate_per_hour__gte=min_rate)

    if is_valid_queryparam(max_rate):
        tutor_qs = tutor_qs.filter(tutorplan__rate_per_hour__lte=max_rate)

    if is_valid_queryparam(expertise) and expertise != 'Choose...':
        tutor_qs = tutor_qs.filter(tutorplan__expertise__name=expertise)

    if is_valid_queryparam(grade) and grade != 'Choose...':
        tutor_qs = tutor_qs.filter(tutorplan__expertise__grade=grade)

    if is_valid_queryparam(name_contains_query):
        tutor_qs = tutor_qs.filter(Q(profile__user__first_name__icontains=name_contains_query) | Q(
            profile__user__last_name__icontains=name_contains_query))

    return tutor_qs


class TutorList(generics.ListAPIView):
    """
    List all tutors.
    """
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TutorSerializer

    def get_queryset(self):
        qs = tutor_filter(self.request)
        return qs


class TutorProfile(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a parent.
    """
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    queryset = ParentProfile.objects.all()
    serializer_class = ParentSerializer

    def get_object(self):
        profile = get_object_or_404(ParentProfile, user=self.request.user)
        return profile

    def perform_update(self, serializer):
        instance = serializer.save(is_tutor=True)


class TutorCreate(generics.CreateAPIView):
    """
    Create a new tutor.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

    def perform_create(self, serializer):
        profile = get_object_or_404(ParentProfile, user=self.request.user)
        profile.is_tutor = True
        profile.save()
        serializer.save(profile=profile)


class TutorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a tutor.
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsTutorOrReadOnly,
    ]

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

    def get_object(self):
        username = self.request.GET.get('username', None)
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(ParentProfile, user=user)
        tutor = get_object_or_404(Tutor, profile=profile)
        return tutor

    # def perform_update(self, serializer):
    #     instance = serializer.save(is_tutor=True)


@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, IsTutor])
def create_tutor_plan(request):
    # request data
    payload = json.loads(request.body)
    major_id = payload['major']
    minor1_id = payload['minor1']
    minor2_id = payload['minor2']
    medium = payload['medium']
    locations = payload['locations']
    rate_per_hour = payload['rate_per_hour']
    try:
        # get objects
        major = get_object_or_404(Expertise, id=major_id)
        minor1 = get_object_or_404(Expertise, id=minor1_id)
        minor2 = get_object_or_404(Expertise, id=minor2_id)
        profile = get_object_or_404(ParentProfile, user=request.user)
        tutor = get_object_or_404(Tutor, profile=profile)

        tutorplan = TutoringPlan.objects.create(
            tutor=tutor,
            major=major,
            minor1=minor1,
            minor2=minor2,
            locations=locations,
            rate_per_hour=rate_per_hour
        )

        return Response({'message': 'Tutoring Plan succesfully Created!'})

    except BaseException as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_traceback = traceback.extract_tb(ex_traceback)
        print(ex_type)
        print(ex_value)
        print(ex_traceback)
        return Response({'message': 'It\'s not you, it\'s us. Please try again.'}, status=500)


class CreateTutorPLan(generics.CreateAPIView):

    permission_classes = [
        permissions.IsAuthenticated
    ]

    queryset = TutoringPlan.objects.all()
    serializer_class = TutoringPlanSerializer

    def perform_create(self, serializer):
        profile = get_object_or_404(ParentProfile, user=self.request.user)
        serializer.save(tutor=profile.tutor)


class TutoringPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated, IsTutorOwnerOrReadOnly
    ]

    serializer_class = TutoringPlanSerializer
    queryset = TutoringPlan.objects.all()

    def get_object(self):
        username = self.request.GET.get('username', None)
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(ParentProfile, user=user)
        tutor = get_object_or_404(Tutor, profile=profile)
        tutor_plan = get_object_or_404(TutoringPlan, tutor=tutor)
        return tutor_plan


class TutorsTutorPlanList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = TutoringPlanSerializer

    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(ParentProfile, user=user)
        tutor = get_object_or_404(Tutor, profile=profile)
        qs = TutoringPlan.objects.filter(tutor=tutor)


class TuTutorRequestList(generics.ListAPIView):
    """
        List all tutor requests from logged in tutor.
    """

    def get_queryset(self):
        tutoringplan = self.request.user.parentprofile.tutor.tutoringplan
        queryset = TutorRequest.objects.filter(
            requested_tutorplan=tutoringplan)
        return queryset

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = TutorRequestSerializer


def tutorplan_filter(request):
    tutorplan_qs = TutoringPlan.objects.all()
    # Parameters to be sent to the backend
    name_contains_query = request.GET.get('name_contains')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    expertise = request.GET.get('expertise')
    location = request.GET.get('location')
    grade = request.GET.get('grade')

    if is_valid_queryparam(min_rate):
        tutorplan_qs = tutorplan_qs.filter(rate_per_hour__gte=min_rate)

    if is_valid_queryparam(max_rate):
        tutorplan_qs = tutorplan_qs.filter(rate_per_hour__lte=max_rate)

    if is_valid_queryparam(expertise) and expertise != 'Choose...':
        tutorplan_qs = tutorplan_qs.filter(expertise__name=expertise)

    if is_valid_queryparam(grade) and grade != 'Choose...':
        tutorplan_qs = tutorplan_qs.filter(expertise__grade=grade)

    if is_valid_queryparam(name_contains_query):
        tutorplan_qs = tutorplan_qs.filter(Q(tutor__profile__user__first_name__icontains=name_contains_query) | Q(
            tutor__profile__user__last_name__icontains=name_contains_query))

    return tutorplan_qs.order_by('?')


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 1


class TutorListPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': math.ceil(self.page.paginator.count/DEFAULT_PAGE_SIZE),
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'results': data
        })


class GeneralTutoringPlanList(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = TutoringPlanSerializer
    pagination_class = TutorListPagination

    def get_queryset(self):
        qs = tutorplan_filter(self.request)
        return qs


class ExpertiseListView(generics.ListAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    serializer_class = ExpertiseSerializer

    def get_queryset(self):
        grade = self.request.GET.get('grade')

        if grade:
            return Expertise.objects.filter(grade__iexact=grade)

        return Expertise.objects.all()


"""
def infinite_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    return Journal.objects.all()[int(offset): int(offset) + int(limit)]


def is_there_more_data(request):
    offset = request.GET.get('offset')
    if int(offset) > Journal.objects.all().count():
        return False
    return True

class ReactInfiniteView(generics.ListAPIView):
    serializer_class = JournalSerializer

    def get_queryset(self):
        qs = infinite_filter(self.request)
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            "journals": serializer.data,
            "has_more": is_there_more_data(request)
        })
"""
