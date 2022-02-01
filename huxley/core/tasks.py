from celery import shared_task
from django.core.exceptions import NON_FIELD_ERRORS
import requests

from django.conf import settings
from requests.exceptions import HTTPError
from huxley.accounts.models import User

from huxley.core.models import Delegate


@shared_task
def poll_waiver(waiver_name, delegate_username_guid):

    # retrieve the waiver id
    headers = {'sw-api-key': settings.SMARTWAIVER_API_KEY}

    try:
        response = requests.get(
            'https://api.smartwaiver.com/v4/webhooks/queues/account', headers=headers)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        return (f'HTTP error occurred: {http_err}')
    except Exception as err:
        return (f'Other error occurred: {err}')
    else:
        response = response.json()
        # print("webhook response:", response)
        if response['api_webhook_account_message_get'] is not None:
            waiver_id, message_id = (response['api_webhook_account_message_get']['payload']['unique_id'],
                                     response['api_webhook_account_message_get']['messageId'])
        else:
            return "error parsing webhook message"

    # check that a new signed waiver exists was retrieved from the queue
    if waiver_id:
        waiver = None

        # retrieve the waiver by waiver id
        headers = {'sw-api-key': settings.SMARTWAIVER_API_KEY}
        try:
            response = requests.get(
                'https://api.smartwaiver.com/v4/waivers/' + waiver_id, headers=headers)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            return (f'HTTP error occurred: {http_err}')
        except Exception as err:
            return (f'Other error occurred: {err}')
        else:
            waiver = response.json()
            # print(waiver)
            if waiver['waiver']['title'] == waiver_name:
                waiver_dict = {
                    'unique_id': waiver['waiver']['waiverId'],
                    'name': waiver['waiver']['firstName'] + ' ' + waiver['waiver']['lastName'],
                    'username': waiver['waiver']['participants'][0]['customParticipantFields'][delegate_username_guid]['value'],
                    'email': waiver['waiver']['email']
                }
            else:
                return "different waivers found in queue"
            # update delegates and create error waiver logs
            print(Delegate.process_waiver(waiver_dict))

            # delete the waiver id by message id
            try:
                response = requests.delete(
                    'https://api.smartwaiver.com/v4/webhooks/queues/account/' + message_id, headers=headers)

                # If the response was successful, no Exception will be raised
                response.raise_for_status()
            except HTTPError as http_err:
                return (f'HTTP error occurred: {http_err}')
            except Exception as err:
                return (f'Other error occurred: {err}')
            else:
                return response.json()

    else:
        return "matching waiver object already exists"
