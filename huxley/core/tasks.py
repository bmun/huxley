from celery import shared_task
import requests

from django.conf import settings
from requests.exceptions import HTTPError

from huxley.core.models import Waiver, Delegate


@shared_task
def poll_waiver():
    waiver_id = get_waiver_id()
    if waiver_id:
        waiver = get_waiver(waiver_id)
        return waiver['waiver']['firstName']

    # return list(Delegate.objects.all().values())


def get_waiver_id():
    headers = {'sw-api-key': settings.SMARTWAIVER_API_KEY}
    # params = {'delete': 'true'}

    try:
        response = requests.get(
            'https://api.smartwaiver.com/v4/webhooks/queues/account', headers=headers)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        response = response.json()
        print("webhook response:", response)
        if response['api_webhook_account_message_get'] is not None:
            return response['api_webhook_account_message_get']['payload']['unique_id']
    return None


def get_waiver(waiver_id):
    headers = {'sw-api-key': settings.SMARTWAIVER_API_KEY}
    try:
        response = requests.get(
            'https://api.smartwaiver.com/v4/waivers/' + waiver_id, headers=headers)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        return response.json()
