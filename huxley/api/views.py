from rest_framework import generics

from huxley.accounts.models import HuxleyUser
from huxley.api.serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HuxleyUser.objects.all()
    serializer_class = UserSerializer
