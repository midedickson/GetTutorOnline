from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.db.models import Q, Count

from .models import Tutor, Expertise, TutoringPlan
from .serializers import TutorSerializer, TutoringPlanSerializer
from .permissions import IsOwnerOrReadOnly
from parents.serializers import TutorRequestSerializer


def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
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
        qs = filter(self.request)
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
        IsOwnerOrReadOnly
    ]

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


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
