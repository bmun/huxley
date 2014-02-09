from django.forms import widgets
from rest_framework import serializers

from huxley.accounts.models import HuxleyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuxleyUser
        fields = ('id', 'user_type', 'school', 'committee')
