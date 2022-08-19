from typing import List

from intuitlib.client import AuthClient

from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects.customer import Customer

from invoice_automation.src.model.school import School
from invoice_automation.src.util import quick_books_utils

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
    auth_client: AuthClient
        OAuth2 authentication client for authenticating to QuickBooks API
    quickbooks_client: QuickBooks
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
        self.auth_client = AuthClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://localhost:8000/callback",
            environment="sandbox"
        )
        try:
            self.quickbooks_client = QuickBooks(
                auth_client=self.auth_client,
                refresh_token=REFRESH_TOKEN,
                company_id=COMPANY_ID
            )
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

    def query_schools_as_customers(self, school_names: List[str]) -> List[School]:
        """
        Looks for existing customers with the same display names as the passed school names

        :param school_names: List of strings containing school names
        :return: List of school objects corresponding to customers which were found
        :raises QuickbooksException:
        """
        try:
            qbCustomers = Customer.choose(school_names, "DisplayName", self.quickbooks_client)
            return [quick_books_utils.get_school_from_customer(customer) for customer in qbCustomers]
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

    def create_customer_from_school(self, school: School) -> None:
        """
        Creates Customer in QuickBooks using passed School

        :param school: School to create Customer from
        :return: None
        :raises QuickbooksException:
        """
        try:
            customer = quick_books_utils.get_customer_from_school(school)
            customer.save(qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

    def update_customer_from_school(self, customer_id: str, school: School) -> None:
        """
        Updates QuickBooks with id# customerId using passed School object

        :param customer_id: QuickBooks Id of Customer to update
        :param school: School object to parse for details to update
        :return: None
        :raises QuickBooksException:
        """
        try:
            customer = quick_books_utils.get_customer_from_school(school)
            customer.Id = customer_id
            customer.save(self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e
