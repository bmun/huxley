import os.path
import re
import datetime
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
from huxley.invoice_automation.src import handler
from huxley.invoice_automation.src.model.address import Address
from huxley.invoice_automation.src.model.conference import Conference
from huxley.invoice_automation.src.model.registration import Registration
from huxley.invoice_automation.src.model.school import School

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1w-Xt-LmWnWvmzDJ6EAp-_I6WCJe9XDlHyAcWOsZ0ZWI'
SAMPLE_RANGE_NAME = 'Responses for Invoicing!A2:K'

TIMESTAMP_REGEX = r"(\d{1,2})\/(\d{1,2})\/(\d{4})"


def main():
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = '../../google_auth_resources/token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = '../../google_auth_resources/credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
    except HttpError as err:
        print(err)

    for row in values:
        print(row)
        process_registration(row)
        print("Invoices sent")


def process_registration(registration: List[str]):
    """
    Called registration handler to handle registration passed from FC spreadsheet
    :param registration:
    [Timestamp, email, phone number, street address, city, state, country, zip-code, num-delegates, school_name, invoice_sent]
    :return:
    """
    registration = [value.strip() for value in registration]
    timestamp, email, phone_number, street_address, city, state, country, zip_code, num_delegates, school_name, invoice_sent = registration

    if invoice_sent == "TRUE":
        return

    address = Address(
        line1=street_address,
        line2="",
        city=city,
        country_sub_division_code=state,
        country=country,
        zip_code=zip_code
    )
    school = School(school_name=school_name, email=email, phone_numbers=[phone_number], address=address)
    reg_datetime = date_from_sheets_timestamp(timestamp)
    reg_object = Registration(
        school=school,
        num_delegates=num_delegates,
        conference=Conference.FC,
        registration_date=reg_datetime
    )
    handler.handle_registration(reg_object)


def date_from_sheets_timestamp(timestamp: str) -> datetime.date:
    date_match = re.match(TIMESTAMP_REGEX, timestamp)
    month, day, year = date_match.groups()
    return datetime.date(int(year), int(month), int(day))


if __name__ == "__main__":
    main()
