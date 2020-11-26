from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class UsersListCreateView(ListCreateAPIView):

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOnlyUserSerializer
        else:
            return WriteOnlyUserSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadOnlyUserSerializer
        else:
            return WriteOnlyUserSerializer



