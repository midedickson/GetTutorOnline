from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from parents.models import ParentProfile
from .models import Tutor, Expertise, TutoringPlan
from .serializers import TutorSerializer, TutoringPlanSerializer, ExpertiseSerializer
from .permissions import IsOwnerOrReadOnly
from parents.serializers import TutorRequestSerializer


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
        tutor_qs = tutor_qs.filter(tutorplan_set__rate_per_hour__gte=min_rate)

    if is_valid_queryparam(max_rate):
        tutor_qs = tutor_qs.filter(tutorplan_set__rate_per_hour__lte=max_rate)

    if is_valid_queryparam(expertise) and expertise != 'Choose...':
        tutor_qs = tutor_qs.filter(tutorplan_set__expertise__name=expertise)

    if is_valid_queryparam(grade) and grade != 'Choose...':
        tutor_qs = tutor_qs.filter(tutorplan_set__expertise__grade=grade)

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
        serializer.save(profile=self.request.user.parentprofile)
    '''
    def create(self, request, *args, **kwargs):
        # Copy parsed content from HTTP request
        data = request.data.copy()

        # Add id of currently logged user
        data['profile'] = request.user.parentprofile_set
        # Default behavior but pass our modified data instead
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    '''


class TutorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a tutor.
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

    def get_object(self):
        username = self.request.query_params.get('username', None)
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(ParentProfile, user=user)
        tutor = get_object_or_404(Tutor, profile=profile)
        return tutor


class TuTutorRequestList(generics.ListAPIView):
    """
        List all tutor requests from logged in tutor.
    """

    def get_queryset(self):
        tutoringplan = self.request.user.parentprofile.tutor.tutoringplan
        queryset = super(ParentTutorRequestList, self).get_queryset()
        queryset = TutorRequest.objects.filter(
            requested_tutorplan=tutoringplan)
        return queryset

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = TutorRequestSerializer


def tutorplan_filter(request):
    tutorplan_qs = TutorPlan.objects.all()
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

    if is_valid_queryparam(expertise and expertise != 'Choose...'):
        tutorplan_qs = tutorplan_qs.filter(expertise__name=expertise)

    if is_valid_queryparam(grade and grade != 'Choose...'):
        tutorplan_qs = tutorplan_qs.filter(expertise__grade=grade)

    if is_valid_queryparam(name_contains_query):
        tutorplan_qs = tutorplan_qs.filter(Q(tutor__profile__user__first_name__icontains=name_contains_query) | Q(
            tutor__profile__user__last_name__icontains=name_contains_query))

    return tutorplan_qs


class GeneralTutoringPlanList(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = TutoringPlanSerializer

    def get_queryset(self):
        qs = tutorplan_filter(self.request)
        return qs


class TutorsTutoringPlan(generics.ListAPIView):
    pass


class TutoringPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = TutoringPlanSerializer
    queryset = TutoringPlan.objects.all()

    def get_object(self):
        username = self.request.query_params.get('username', None)
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(ParentProfile, user=user)
        tutor = get_object_or_404(Tutor, profile=profile)
        tutor_plan = get_object_or_404(TutoringPlan)
        return tutor_plan


class ExpertiseListView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = ExpertiseSerializer

    queryset = Expertise.objects.all()


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
