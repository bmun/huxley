# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.db import transaction

from rest_framework import generics, response, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied

from huxley.api.serializers import CreateUserSerializer, RegistrationSerializer
from huxley.core.models import Conference, School


class Register(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, )
    serializer_classes = {
        'user': CreateUserSerializer,
        'registration': RegistrationSerializer
    }

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if Conference.get_current().open_reg:
            return self.register(request, *args, **kwargs)
        raise PermissionDenied('Conference registration is closed.')

    def register(self, request, *args, **kwargs):
        user_data = request.data['user']
        registration_data = request.data['registration']

        with transaction.atomic():
            user_serializer = self.serializer_classes['user'](data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            school_id = user_serializer.data['school']['id']
            registration_data['school'] = school_id
            registration_serializer = self.serializer_classes['registration'](data=registration_data)
            registration_serializer.is_valid(raise_exception=True)
            registration_serializer.save()

        data = {'user': user_serializer.data,
                    'registration': registration_serializer.data}
        return response.Response(data, status=status.HTTP_200_OK)
