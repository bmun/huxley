# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.conf import settings
from django.contrib.auth import login, logout
from django.http import Http404

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import (APIException, AuthenticationFailed,
                                       PermissionDenied)
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from huxley.accounts.models import User
from huxley.accounts.exceptions import AuthenticationError, PasswordChangeFailed
from huxley.api.permissions import DelegateUserPasswordPermission, IsPostOrSuperuserOnly, IsUserOrSuperuser
from huxley.api.serializers import CreateUserSerializer, UserSerializer
from huxley.core.models import Conference, School


class UserList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = User.objects.all()
    permission_classes = (IsPostOrSuperuserOnly, )

    def create(self, request, *args, **kwargs):
        if Conference.get_current().open_reg:
            return super(UserList, self).create(request, *args, **kwargs)
        raise PermissionDenied('Conference registration is closed.')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrSuperuser, )


class CurrentUser(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, )

    def get(self, request, *args, **kwargs):
        '''Get the current user if they're authenticated.'''
        if not request.user.is_authenticated:
            raise Http404
        return Response(UserSerializer(request.user).data)

    def post(self, request, *args, **kwargs):
        '''Log in a new user.'''
        print('post request')
        print(request.user)
        print(request.data)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            raise PermissionDenied('Another user is currently logged in.')

        try:
            data = request.data
            user = User.authenticate(data['username'], data['password'])
        except AuthenticationError as e:
            raise AuthenticationFailed(str(e))

        login(request, user)
        return Response(
            UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        '''Log out the currently logged-in user.'''
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


class UserPassword(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, )

    def post(self, request, *args, **kwargs):
        '''Reset a user's password and email it to them.'''
        try:
            username = request.data.get('username', '')
            User.reset_password(username=username)
            return Response({}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        '''Change the authenticated user's password.'''
        if not request.user.is_authenticated:
            raise PermissionDenied()

        data = request.data
        password, new_password = data.get('password'), data.get('new_password')

        try:
            request.user.change_password(password, new_password)
            return Response({}, status=status.HTTP_200_OK)
        except PasswordChangeFailed as e:
            raise APIException(str(e))


class DelegateUserPassword(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (DelegateUserPasswordPermission, )

    def post(self, request, *args, **kwargs):
        '''Reset a delegate's password and email it to them.'''
        try:
            delegate_id = request.data.get('delegate_id', -1)
            user = User.objects.get(delegate__id=delegate_id)
            User.reset_password(user=user)
            return Response({}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            raise Http404
