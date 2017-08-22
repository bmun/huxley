# Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied

from huxley.api import mixins
from huxley.api.serializers import CreateUserSerializer, RegistrationSerializer
from huxley.core.models import Conference


class Register(generics.GenericAPIView, mixins.RegisterMixin):
	authentication_classes = (SessionAuthentication, )
	serializer_classes = {
		'user': CreateUserSerializer,
		'registration': RegistrationSerializer
	}

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		if Conference.get_current().open_reg:
			return super(Register, self).create(request, *args, **kwargs)
		raise PermissionDenied('Conference registration is closed.')
