from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from .permissions import IsOwner
from django.shortcuts import get_object_or_404


class ParentCreate(generics.CreateAPIView):
    """
    Create a new parent.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]

    queryset = ParentProfile.objects.all()
    serializer_class = ParentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    '''
    def create(self, request, *args, **kwargs):
        # Copy parsed content from HTTP request
        data = request.data.copy()

        # Add id of currently logged user
        data['user'] = request.user.username
        print(data)

        # Default behavior but pass our modified data instead
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    '''


class ParentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a parent.
    """
    permission_classes = [
        IsOwner,
    ]

    queryset = ParentProfile.objects.all()
    serializer_class = ParentSerializer

    def get_object(self):
        username = self.request.user
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(ParentProfile, user=user)
        return profile


class TutorRequestCreate(generics.CreateAPIView):
    """
        Send Request to tutor
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]

    queryset = TutorRequest.objects.all()
    serializer_class = TutorRequestSerializer

    def create(self, request, *args, **kwargs):
        # Copy parsed content from HTTP request
        data = request.data.copy()

        # Add profile of currently logged user
        data['requested_by'] = request.user.parentprofile.id

        # Default behavior but pass our modified data instead
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TutorRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a tutor request
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]

    queryset = TutorRequest.objects.all()
    serializer_class = TutorRequestSerializer


class ParentTutorRequestList(generics.ListAPIView):
    """
        List all tutor requests from logged in parent.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = TutorRequestSerializer

    def get_queryset(self):
        profile = self.request.user.parentprofile
        queryset = TutorRequest.objects.filter(requested_by=profile)
        return queryset


# class SpecialRequestCreate(generics.CreateAPIView):
#     """
#         Create Special Request
#     """

#     permission_classes = [
#         permissions.IsAuthenticated
#     ]

#     queryset = SpecialRequest.objects.all()
#     serializer_class = SpecialRequestSerializer

#     def create(self, request, *args, **kwargs):
#         # Copy parsed content from HTTP request
#         data = request.data.copy()

#         # Add id of currently logged user
#         data['requested_by'] = request.user.id

#         # Default behavior but pass our modified data instead
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class UpdateSpecialRequest(generics.RetrieveUpdateDestroyAPIView):
#     """
#         Update Special Request
#     """
#     permission_classes = [
#         permissions.IsAuthenticated, IsOwner
#     ]

#     queryset = SpecialRequest.objects.all()
#     serializer_class = SpecialRequestSerializer


# class ChildCreate(generics.CreateAPIView):
#     """
#         Regiser Children
#     """

#     permission_classes = [
#         permissions.IsAuthenticated
#     ]

#     queryset = Child.objects.all()
#     serializer_class = ChildSerializer

#     def create(self, request, *args, **kwargs):
#         # Copy parsed content from HTTP request
#         data = request.data.copy()

#         # Add id of currently logged user
#         data['parent'] = request.user.id

#         # Default behavior but pass our modified data instead
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
