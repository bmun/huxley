import datetime
from typing import List, Dict

from intuitlib.client import AuthClient

from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Invoice, Ref, Item, EmailAddress, PhoneNumber, DetailLine
from quickbooks.objects.customer import Customer

from invoice_automation.src.authentication.authenticator import Authenticator
from invoice_automation.src.model.conference import Conference
from invoice_automation.src.model.fee_type import FeeType
from invoice_automation.src.model.registration import Registration
from invoice_automation.src.model.school import School
from invoice_automation.src.util import quick_books_utils

# TODO: Replace with prod versions during deployment
# Should probably move these to settings/main.py at some point
# Quickbooks constants
from invoice_automation.src.util.query_utils import construct_invoice_query
from invoice_automation.src.util.quick_books_utils import check_invoice_matches_items_and_counts, create_SalesItemLine, \
    get_due_date_from_conference_fee_type_reg_time

DISPLAY_NAME = "DisplayName"
SCHOOL_FEE = "School Fee"
DELEGATE_FEE = "Delegate Fee"


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
            refresh_token="",
            realm_id="",
            access_token=""
    ) -> None:
        """
        Instantiates authClient using hardcoded CLIENT_ID and CLIENT_SECRET
        then uses it to instantiate a QuickBooks instance

        Raises
        ------
        QuickbooksException
        """
        if len(refresh_token) == 0:
            authenticator = Authenticator(client_id=client_id, client_secret=client_secret)
            self.auth_client = authenticator.authenticate()
        else:
            self.auth_client = AuthClient(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=Authenticator.REDIRECT_URI,
                environment=Authenticator.ENVIRONMENT,
                access_token=access_token
            )
        try:
            self.quickbooks_client = QuickBooks(
                auth_client=self.auth_client,
                refresh_token=refresh_token,
                company_id=realm_id,
            )
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

    # Customer methods:

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

    def update_or_create_customer_from_school(self, school: School) -> Customer:
        """
        Creates or updates Customer in QuickBooks using passed school
        Uses existing customer id and sync token when updating

        :param school:
        :return:
        """
        existing_customer = self.get_customer_from_school(school)
        new_customer = quick_books_utils.get_customer_from_school(school)

        if existing_customer:
            new_customer.Id = existing_customer.Id
            new_customer.SyncToken = existing_customer.SyncToken

        try:
            new_customer.save(qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

        return new_customer

    def get_customer_from_school(self, school: School) -> Customer | None:
        """
        Gets the customer object corresponding to the passed school by matching display name

        :param school:
        :return:
        """
        try:
            customer_matches = Customer.choose([school.school_name], field="DisplayName", qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

        if len(customer_matches) < 1:
            return None
        return customer_matches[0]

    def get_customer_ref_from_school(self, school: School | None) -> Ref | None:
        """
        Gets a CustomerRef object from a School object, for use in other objects, such as invoices
        Query for a customer with a matching name, and uses its toref method

        :param school:
        :return:
        """
        if school is None:
            return None

        customer = self.get_customer_from_school(school)
        if customer is None:
            return None
        return customer.to_ref()

    # Invoice methods:

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

    def query_invoices_from_registration(self, registration: Registration) -> Dict[str, Invoice] | None:
        """
        Queries Quickbooks to see if matching invoices already exist
        An invoice is considered matching if all the following conditions are met:
        - Customer matches school on registration
        - Line items correspond to conference on registration
        - Delegate fee quantity matches registration's number of delegates
        If existing, we expect two invoices, one for school fee and one for delegate fee
        If they do, returns the two invoices, otherwise, returns None
        We only expect two invoices at most to match
        TODO: See if invoices can be filtered by line items (the issue is we can't use JOINs)
        :param registration: Registration to match against
        :return: Matching invoices, None if none are found
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
        fee_to_invoice = {}
        delegate_fee_line_item_name, school_fee_line_item_name \
            = quick_books_utils.CONFERENCE_TO_LINE_ITEM_NAMES[registration.conference]
        for invoice in invoices:
            if check_invoice_matches_items_and_counts(
                    invoice,
                    [delegate_fee_line_item_name],
                    [registration.num_delegates]
            ):
                fee_to_invoice[DELEGATE_FEE] = invoice
            elif check_invoice_matches_items_and_counts(
                invoice,
                [school_fee_line_item_name],
                [1]
            ):
                fee_to_invoice[SCHOOL_FEE] = invoice
        if fee_to_invoice:
            return fee_to_invoice
        else:
            return None

    def create_invoices_from_registration(self, registration: Registration, email: str) -> Dict[str, Invoice]:
        """
        Creates invoice in Quickbooks from passed registration
        Note: Does not check to see if a matching invoice already exists
        :param email:
        :param registration:
        :return:
        """
        # get customer_ref
        customer_ref = self.get_customer_ref_from_school(registration.school)
        # create line items
        items = self.query_line_items_from_conference(registration.conference)
        invoices = {}
        service_date = quick_books_utils.SERVICE_DATES[registration.conference]
        for item in items:
            if SCHOOL_FEE in item.Name:
                invoices[SCHOOL_FEE] = self.create_invoice(
                    customer_ref,
                    [create_SalesItemLine(item, 1, service_date)],
                    email,
                    get_due_date_from_conference_fee_type_reg_time(
                        registration.registration_date,
                        FeeType.SCHOOL_FEE,
                        registration.conference
                    )
                )
            elif DELEGATE_FEE in item.Name:
                invoices[DELEGATE_FEE] = self.create_invoice(
                    customer_ref,
                    [create_SalesItemLine(item, registration.num_delegates, service_date)],
                    email,
                    get_due_date_from_conference_fee_type_reg_time(
                        registration.registration_date,
                        FeeType.DELEGATE_FEE,
                        registration.conference
                    )
                )
        return invoices

    def create_invoice(self,
                       customer_ref: Ref,
                       lines: List[DetailLine],
                       email: str,
                       due_date: datetime.date) -> Invoice:
        """
        Creates a new invoice in quickbooks with passed metadata
        Does not check to see if matching invoice already exists
        :param due_date:
        :param customer_ref:
        :param lines:
        :param email:
        :return: Created invoice
        """
        invoice = Invoice()
        invoice.CustomerRef = customer_ref
        invoice.Line = lines

        invoice.BillEmail = EmailAddress()
        invoice.BillEmail.Address = email
        invoice.EmailStatus = "NeedToSend"

        invoice.DueDate = due_date.isoformat()

        try:
            invoice.save(qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

        return invoice

    def send_invoice(self, invoice: Invoice):
        """
        Sends invoice to email address specified in passed invoice
        :param invoice:
        :return:
        """
        try:
            invoice.send(qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e

    # Item methods

    def query_line_items_from_conference(self, conference: Conference) -> List[Item]:
        """
        Query QuickBooks for items corresponding to the passed conference

        :param conference:
        :return:
        """
        item_names = quick_books_utils.CONFERENCE_TO_LINE_ITEM_NAMES[conference]

        try:
            return Item.choose(item_names, field="Name", qb=self.quickbooks_client)
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)
            raise e
