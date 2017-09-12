# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

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
        user_serializer = self.serializer_classes['user'](data=user_data)
        is_user_valid = user_serializer.is_valid()

        registration_data = request.data['registration']
        registration_serializer = self.serializer_classes['registration'](
            data=registration_data)
        is_registration_valid = registration_serializer.is_registration_valid()

        if is_user_valid and is_registration_valid:
            user_serializer.save()
            school_id = School.objects.get(name=user_data['school']['name']).id
            registration_data['school'] = school_id
            registration_serializer = self.serializer_classes['registration'](
                data=registration_data)
            registration_serializer.is_valid()
            registration_serializer.save()
            data = {'user': user_serializer.data,
                    'registration': registration_serializer.data}
            response_status = status.HTTP_200_OK
        else:
            data = registration_serializer.errors.copy()
            data.update(user_serializer.errors)
            response_status = status.HTTP_400_BAD_REQUEST

        return response.Response(data, status=response_status)
