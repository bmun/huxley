from django.conf import settings
from django.contrib.auth.models import User

class LoginAsUserBackend:
    def authenticate(self, username=None, password=None):
        if settings.ADMIN_SECRET and password == settings.ADMIN_SECRET:
            try:
                return User.objects.get(username=username)
            except:
                pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
