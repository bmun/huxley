# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

import json

from rest_framework import status
from rest_framework.response import Response

class ListUpdateModelMixin(object):
    """
    Update a queryset
    """

    def list_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        # I feel like there should be a cleaner way to do what the next
        # two lines are trying to do. Any suggestions would be appreciated.
        items = json.loads(request.data.items()[0][0])
        self.lookup_url_kwarg = 'obj_id'

        for item in items:
            self.kwargs[self.lookup_url_kwarg] = item['id']
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=item, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_list_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def perform_list_update(self, serializer):
        serializer.save()

    def partial_list_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.list_update(request, *args, **kwargs)
