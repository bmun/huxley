import os

import django
from django.conf import settings

from huxley.invoice_automation.src.handler.registration_handler import RegistrationHandler

# Set the default Django settings module to access Intuit authentication constants
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huxley.settings')

django.setup()

handler = RegistrationHandler(
    settings.CLIENT_ID,
    settings.CLIENT_SECRET,
    settings.REFRESH_TOKEN,
    settings.REALM_ID,
    settings.ACCESS_TOKEN
)
print(handler)
