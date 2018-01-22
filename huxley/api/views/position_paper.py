# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser

from huxley.api import permissions
from huxley.api.serializers import PositionPaperSerializer
from huxley.core.models import PositionPaper

from django.http.response import HttpResponse

class PositionPaperDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication, )
    # parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.PositionPaperDetailPermission, )
    queryset = PositionPaper.objects.all()
    serializer_class = PositionPaperSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class PositionPaperFile(generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication, )

    def retrieve(self, request, *args, **kwargs):
        file_path = request.GET.get('file', None)
        if file_path:
            file_name = file_path.split('/')[-1]
            with open('position_papers/'+file_name, 'r') as f:
                data = f.read()
            response = HttpResponse(data, status=status.HTTP_201_CREATED)
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachement; file_name="{0}"'.format(file_name)
        return Response({}, status=status.HTTP_200_OK)
