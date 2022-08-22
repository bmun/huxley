import datetime
from typing import List

from intuitlib.client import AuthClient

from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Invoice, Ref, Item
from quickbooks.objects.customer import Customer

from invoice_automation.src.model.conference import Conference
from invoice_automation.src.model.registration import Registration
from invoice_automation.src.model.school import School
from invoice_automation.src.util import quick_books_utils

# TODO: Replace with prod versions during deployment
# Should probably move these to settings/main.py at some point
# Quickbooks constants
from invoice_automation.src.util.query_utils import construct_invoice_query
from invoice_automation.src.util.quick_books_utils import check_invoice_matches_items_and_counts

CLIENT_ID = "ABYdHrqfKuQBK7bDiZpCK9C6Cq9bhayJJZbPCRyJLu7rO2nNqX"
CLIENT_SECRET = "KKJQ9uQJdlydvcCZigkZ3PlbEXQ8ZUjohKrEwzjN"
COMPANY_ID = "4620816365199192370"

# Quickbooks tokens
REFRESH_TOKEN = "AB11669491025T4PgHV7qio9chs0pTSBkNE2TIXoHq8Xx0YQ70"

REDIRECT_URI = "http://localhost:8000/callback"
SANDBOX = "sandbox"

DISPLAY_NAME = "DisplayName"

# Query templates
CUSTOMER_REF_VALUE_WHERE_TEMPLATE = "CustomerRef.value = '{}'"
CUSTOMER_REF_NAME_WHERE_TEMPLATE = "CustomerRef.name = '{}'"
INVOICE_FILTER_START_DATE = datetime.datetime(2022, 8, 1)
INVOICE_FILTER_START_DATE_FORMAT = "%Y-%m-%dT%X%z"
INVOICE_FILTER_START_DATE_WHERE_TEMPLATE = "MetaData.CreateTime >= '{}'"
INVOICE_QUERY_TEMPLATE = "SELECT * FROM Invoice WHERE {}"


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

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            environment: str,
            refresh_token: str,
            company_id: str
    ) -> None:
        """
        Instantiates authClient using hardcoded CLIENT_ID and CLIENT_SECRET
        then uses it to instantiate a QuickBooks instance

        Raises
        ------
        QuickbooksException
        """
        self.auth_client = AuthClient(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            environment=environment
        )
        try:
            self.quickbooks_client = QuickBooks(
                auth_client=self.auth_client,
                refresh_token=refresh_token,
                company_id=company_id
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
            qbCustomers = Customer.choose(school_names, DISPLAY_NAME, self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

        return [quick_books_utils.get_school_from_customer(customer) for customer in qbCustomers]

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
            customer.save(qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

    def get_customer_ref_from_school(self, school: School | None) -> Ref | None:
        """
        Gets a CustomerRef object from a School object, for use in other objects, such as invoices
        Query for a customer with a matching name, and uses its toref method

        :param school:
        :return:
        """
        if school is None:
            return None

        try:
            customer_matches = Customer.choose([school.school_name], field="DisplayName", qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

        if len(customer_matches) < 1:
            return None
        return customer_matches[0].to_ref()

    def query_invoices_from_customer_ref(self, customer_ref: Ref) -> List[Invoice] | None:
        """
        Queries Quickbooks for invoices which were billed to the passed customer
        Filters queries for those from the past year
        :param customer_ref:
        :return: non-empty list of Invoices or None
        """
        # construct query
        query = construct_invoice_query(customer_ref)
        # issue query
        try:
            invoices = Invoice.query(query, qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

        if len(invoices) < 1:
            return None
        return invoices

    def query_invoice_from_registration(self, registration: Registration) -> Invoice | None:
        """
        Queries Quickbooks to see if a matching invoice already exists
        An invoice is considered matching if all the following conditions are met:
        - Customer matches school on registration
        - Line items correspond to conference on registration
        - Delegate fee quantity matches registration's number of delegates
        If it does, it returns the invoice, otherwise, it returns None
        We only expect one invoice at most to match
        TODO: See if invoices can be filtered by line items (the issue is we can't use JOINs)
        :param registration: Registration to match against
        :return: Matching invoice, None if one is not found
        """
        if registration is None:
            return registration

        try:
            # construct CustomerRef
            customer_ref = self.get_customer_ref_from_school(registration.school)
            # issue invoice query
            invoices = self.query_invoices_from_customer_ref(customer_ref)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

        if invoices is None:
            return None
        # get line items
        item_names = quick_books_utils.CONFERENCE_TO_LINE_ITEM_NAMES[registration.conference]
        item_counts = [registration.num_delegates, 1]
        for invoice in invoices:
            if check_invoice_matches_items_and_counts(invoice, item_names, item_counts):
                return invoice
        return None

    def query_line_items_from_conference(self, conference: Conference) -> List[Item]:
        item_names = quick_books_utils.CONFERENCE_TO_LINE_ITEM_NAMES[conference]

        try:
            return Item.choose(item_names, field="Name", qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e
