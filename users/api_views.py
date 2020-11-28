from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from .permissions import ReadOnly
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class UsersListCreateView(ListCreateAPIView):

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOnlyUserSerializer
        else:
            return WriteOnlyUserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOnlyUserSerializer
        else:
            return WriteOnlyUserSerializer



