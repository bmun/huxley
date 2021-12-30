from celery import shared_task
from django.core.exceptions import NON_FIELD_ERRORS
import requests

from django.conf import settings
from requests.exceptions import HTTPError
from huxley.accounts.models import User

from huxley.core.models import Waiver


@shared_task
def poll_waiver():
    waiver_id, message_id = get_waiver_id()
    # check that a new signed waiver exists in the queue that is not yet processed
    if waiver_id and not Waiver.objects.filter(unique_id=waiver_id).exists():
        waiver = get_waiver(waiver_id)
        return create_waiver_and_update_delegate(waiver, message_id)


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
            return (response['api_webhook_account_message_get']['payload']['unique_id'],
                    response['api_webhook_account_message_get']['messageId'])
    return (None, None)


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


def create_waiver_and_update_delegate(waiver, message_id):
    unique_id = waiver['waiver']['waiverId']
    first_name = waiver['waiver']['firstName']
    last_name = waiver['waiver']['lastName']
    name = first_name + ' ' + last_name
    username = waiver['waiver']['participants'][0]['customParticipantFields']['61ccf3af74569']['value']

    # validate the waiver to a user's username
    users_list = list(User.objects.filter(username=username))
    print("users matched:", users_list)

    delegate = None

    if len(users_list) == 1 and users_list[0].is_delegate():
        delegate = users_list[0].delegate
        print(delegate)
        # validate the waiver to that user's Delegate by name
        if not delegate.name == name:
            delegate = None

    # Create the waiver object with a foreign key
    new_waiver = Waiver(unique_id=unique_id, name=name, delegate=delegate)
    new_waiver.save()

    # update the delegate's waiver submitted
    if delegate:
        delegate.waiver_submitted = True
        delegate.save()

    return new_waiver.name

    # delete the waiver message
