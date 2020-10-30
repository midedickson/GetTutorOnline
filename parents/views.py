from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from .permissions import IsOwner, IsRequester
from django.shortcuts import get_object_or_404
import sys
import traceback
import os


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
        profile = get_object_or_404(ParentProfile, user=self.request.user)
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

    def perform_create(self, serializer):
        profile = ParentProfile.objects.get(user=self.request.user)
        serializer.save(requested_by=profile)


class TutorRequestDetail(generics.RetrieveDestroyAPIView):
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


@api_view(["GET"])
@permission_classes([IsRequester, ])
def cancel_after24hrs(request, pk):
    try:
        tutor_request = TutorRequest.objects.get(id=pk)
    except TutorRequest.DoesNotExist:
        return Response({'message': 'This tutor request does not exist'}, status=404)
    else:
        try:
            print(tutor_request.requested_by)
            if tutor_request.isAccepted == True:
                return Response({'message': 'The tutor has already accepted this request. Please Proceed to payment'}, status=400)
            if tutor_request.isCancelled == False:
                tutor_request.isCancelled = True
                tutor_request.save()
                return Response({'message': 'Request has been cancelled as the Tutor has not accepted after 24 hours'}, status=200)
            if tutor_request.isCancelled == True:
                return Response({'message': 'This tutor request has already been cancelled earlier'}, status=400)

        except BaseException as e:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            ex_traceback = traceback.extract_tb(ex_traceback)
            print(ex_type)
            print(ex_value)
            print(ex_traceback)
            return Response({'message': 'It\'s not you, it\'s us. Please try again.'}, status=500)
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
