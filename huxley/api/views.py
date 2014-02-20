from rest_framework import generics, permissions

from huxley.accounts.models import HuxleyUser
from huxley.api.permissions import IsUserOrSuperuser
from huxley.api.serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrSuperuser,)
