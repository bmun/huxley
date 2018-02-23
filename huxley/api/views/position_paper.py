# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from datetime import date

from django.db import transaction
from django.http.response import HttpResponse

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FileUploadParser, FormParser, JSONParser, MultiPartParser

from huxley.api import permissions
from huxley.api.serializers import PositionPaperSerializer
from huxley.core.models import PositionPaper


class PositionPaperDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.PositionPaperDetailPermission, )
    queryset = PositionPaper.objects.all()
    serializer_class = PositionPaperSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response(
                "POST endpoint only used for file upload.",
                status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        instance = PositionPaper.objects.get(id=kwargs['pk'])
        response_data = []
        data = {'file': file}

        if request.user.is_delegate():
            data['submission_date'] = date.today()

        with transaction.atomic():
            serializer = self.get_serializer(
                instance=instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PositionPaperFile(generics.RetrieveAPIView):
    authentication_classes = (SessionAuthentication, )

    def retrieve(self, request, *args, **kwargs):
        paper_id = request.GET.get('id', -1)
        if paper_id < 0:
            return Response(
                "Must supply paper id.", status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = PositionPaper.objects.get(id=paper_id)
            file_path = instance.file.name
            if file_path:
                with open(file_path, 'r') as f:
                    data = f.read()
                response = HttpResponse(data, status=status.HTTP_201_CREATED)
                response['Content-Type'] = 'text/plain'
                file_name = file_path.split('/')[-1]
                response[
                    'Content-Disposition'] = 'attachement; file_name="{0}"'.format(
                        file_name.encode("utf8"))
            else:
                response = HttpResponse({}, status=status.HTTP_200_OK)
            return response
        except PositionPaper.DoesNotExist:
            return Response(
                "Paper with id {0} does not exist".format(paper_id),
                status=status.HTTP_400_BAD_REQUEST)
