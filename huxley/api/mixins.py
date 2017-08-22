# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from huxley.core.models import Delegate, School


class RegisterMixin(object):
    """
    Mixin customized to create necessary model instances when registering
    """

    def create(self, request, *args, **kwargs):
        user_data = request.data['user']
        registration_data = request.data['registration']
        user_serializer = self.serializer_classes['user'](data=user_data)
        registration_serializer = self.serializer_classes['registration'](
            data=registration_data)
        is_user_valid = user_serializer.is_valid()
        is_registration_valid = self.is_registration_valid(
            registration_serializer)

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

        return Response(data, status=response_status)

    def is_registration_valid(self, registration_serializer):
        registration_serializer.is_valid()
        errors = registration_serializer.errors
        return len(errors) == 1 and 'school' in errors


class ListUpdateModelMixin(object):
    """
    Update a queryset
    """

    def list_update(self, request, partial=False, *args, **kwargs):
        updates = {delegate['id']: delegate for delegate in request.data}
        response_data = []

        with transaction.atomic():
            delegates = Delegate.objects.filter(id__in=updates.keys())
            for delegate in delegates:
                serializer = self.get_serializer(
                    instance=delegate,
                    data=updates[delegate.id],
                    partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response_data.append(serializer.data)

        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return self.list_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.list_update(request, partial=True, *args, **kwargs)
