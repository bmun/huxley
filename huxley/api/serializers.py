from django.forms import widgets
from rest_framework import serializers

from huxley.accounts.models import HuxleyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuxleyUser
        fields = ('id', 'first_name', 'last_name', 'user_type', 'school',
                  'committee')
