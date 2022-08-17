from typing import List

from intuitlib.client import AuthClient

from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects.customer import Customer
from invoice_automation.src.model.School import School
from invoice_automation.src.util import QuickBooksUtils


# TODO: Replace with prod versions during deployment
# Should probably move these to settings/main.py at some point
# Quickbooks constants

CLIENT_ID = "ABYdHrqfKuQBK7bDiZpCK9C6Cq9bhayJJZbPCRyJLu7rO2nNqX"
CLIENT_SECRET = "KKJQ9uQJdlydvcCZigkZ3PlbEXQ8ZUjohKrEwzjN"
COMPANY_ID = "4620816365199192370"

# Quickbooks tokens
REFRESH_TOKEN = "AB11669491025T4PgHV7qio9chs0pTSBkNE2TIXoHq8Xx0YQ70"


class QuickBooksModule:
    """
    Abstraction barrier for calling QuickBook API's

    Attributes
    ----------
    authClient: AuthClient
        OAuth2 authentication client for authenticating to QuickBooks API
    quickBooksClient: QuickBooks
        QuickBooksClient which makes actual API calls to QuickBooks

    Methods
    -------
    querySchoolsAsCustomers(schoolNames: List[str]) -> List[School]:
        Looks for already registered schools using their names
    """

    def __init__(self) -> None:
        """
        Instantiates authClient using hardcoded CLIENT_ID and CLIENT_SECRET
        then uses it to instantiate a QuickBooks instance

        Raises
        ------
        QuickbooksException
        """
        self.authClient = AuthClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://localhost:8000/callback",
            environment="sandbox"
        )
        try:
            self.quickBooksClient = QuickBooks(
                auth_client=self.authClient,
                refresh_token=REFRESH_TOKEN,
                company_id=COMPANY_ID
            )
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

    def querySchoolsAsCustomers(self, schoolNames: List[str]) -> List[School]:
        """
        Looks for existing customers with the same display names as the passed school names

        :param schoolNames: List of strings containing school names
        :return: List of school objects corresponding to customers which were found
        """
        try:
            qbCustomers = Customer.choose(schoolNames, "DisplayName", self.quickBooksClient)
            return [QuickBooksUtils.getSchoolFromCustomer(customer) for customer in qbCustomers]
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e


qbm = QuickBooksModule()
schools = qbm.querySchoolsAsCustomers(["Kookies by Kathy", "Mark Cho"])
for s in schools:
    print(s.phoneNumbers[0].FreeFormNumber)
