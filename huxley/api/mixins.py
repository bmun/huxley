# Copyright (c) 2011-2022 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from huxley.core.models import Delegate


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
