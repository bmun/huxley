# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.contrib.auth import login, logout
from django.http import Http404

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import (APIException, AuthenticationFailed,
                                       PermissionDenied)
from rest_framework.response import Response

from huxley.accounts.models import User
from huxley.accounts.exceptions import AuthenticationError, PasswordChangeFailed
from huxley.api.permissions import IsPostOrSuperuserOnly, IsUserOrSuperuser
from huxley.api.serializers import CreateUserSerializer, UserSerializer


class UserList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = User.objects.all()
    permission_classes = (IsPostOrSuperuserOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrSuperuser,)


class CurrentUser(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, *args, **kwargs):
        '''Get the current user if they're authenticated.'''
        if not request.user.is_authenticated():
            raise Http404
        return Response(UserSerializer(request.user).data)

    def post(self, request, *args, **kwargs):
        '''Log in a new user.'''
        if request.user.is_authenticated():
            raise PermissionDenied('Another user is currently logged in.')

        try:
            data = request.DATA
            user = User.authenticate(data['username'], data['password'])
        except AuthenticationError as e:
            raise AuthenticationFailed(str(e))

        login(request, user)
        return Response(UserSerializer(user).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        '''Log out the currently logged-in user.'''
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPassword(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)

    def put(self, request, *args, **kwargs):
        '''Change the authenticated user's password.'''
        if not request.user.is_authenticated():
            raise PermissionDenied()

        data = request.DATA
        password, new_password = data.get('password'), data.get('new_password')

        try:
            request.user.change_password(password, new_password)
            return Response(status=status.HTTP_200_OK)
        except PasswordChangeFailed as e:
            raise APIException(str(e))
