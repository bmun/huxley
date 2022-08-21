from typing import List
from unittest.mock import patch, Mock, call

import pytest
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Customer

from invoice_automation.src.model.school import School
from invoice_automation.src.module.quick_books_module import QuickBooksModule, DISPLAY_NAME
from invoice_automation.tst.paths import AUTHCLIENT_PATH, QUICKBOOKS_CLIENT_PATH, CUSTOMER_CHOOSE_PATH, \
    GET_SCHOOL_FROM_CUSTOMER_PATH, GET_CUSTOMER_FROM_SCHOOL_PATH

CLIENT_ID = "CLIENT"
CLIENT_SECRET = "SECRET"
REDIRECT_URI = "http://redirect_here"
ENVIRONMENT = "Environment"
REFRESH_TOKEN = "REFRESHING"
COMPANY_ID = "BMUN LLC"
QUICKBOOKS_CLIENT_CREATION_FAILED = "QuickBooks client couldn't be created"
SCHOOL_NAMES = ["Cal", "Berkeley", "UCB"]
ERROR_MESSAGE = "Quickbooks Error"
QUICKBOOKS_EXCEPTION = QuickbooksException(ERROR_MESSAGE)
CUSTOMER_ID = "Customer"


class TestQuickBooksModule:
    @pytest.fixture
    def mock_auth_client(self) -> AuthClient:
        return Mock(spec=AuthClient)

    @pytest.fixture
    def mock_quickbooks_client(self) -> QuickBooks:
        return Mock(spec=QuickBooks)

    @patch(AUTHCLIENT_PATH)
    @patch(QUICKBOOKS_CLIENT_PATH)
    def test_init_happyPath(self,
                            quickbooks_client_patch: Mock,
                            authclient_patch: Mock,
                            mock_auth_client: AuthClient,
                            mock_quickbooks_client: QuickBooks):
        # Setup
        authclient_patch.return_value = mock_auth_client
        quickbooks_client_patch.return_value = mock_quickbooks_client

        # Act
        qbm = QuickBooksModule(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ENVIRONMENT, REFRESH_TOKEN, COMPANY_ID)

        # Verify
        authclient_patch.assert_called_once_with(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            environment=ENVIRONMENT
        )
        assert qbm.auth_client == mock_auth_client
        quickbooks_client_patch.assert_called_once_with(
            auth_client=mock_auth_client,
            refresh_token=REFRESH_TOKEN,
            company_id=COMPANY_ID
        )
        assert qbm.quickbooks_client == mock_quickbooks_client

    @patch(AUTHCLIENT_PATH)
    @patch(QUICKBOOKS_CLIENT_PATH)
    def test_init_quickbooksThrows(self,
                                   quickbooks_client_patch: Mock,
                                   authclient_patch: Mock,
                                   mock_auth_client: AuthClient):
        # Setup
        authclient_patch.return_value = mock_auth_client
        quickbooks_client_patch.side_effect = QuickbooksException(QUICKBOOKS_CLIENT_CREATION_FAILED)

        # Act
        try:
            qbm = QuickBooksModule(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ENVIRONMENT, REFRESH_TOKEN, COMPANY_ID)
        except QuickbooksException as e:
            exn = e

        # Verify
        authclient_patch.assert_called_once_with(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            environment=ENVIRONMENT
        )
        quickbooks_client_patch.assert_called_once_with(
            auth_client=mock_auth_client,
            refresh_token=REFRESH_TOKEN,
            company_id=COMPANY_ID
        )
        assert isinstance(exn, QuickbooksException)
        assert exn.message == QUICKBOOKS_CLIENT_CREATION_FAILED

    @pytest.fixture
    @patch(AUTHCLIENT_PATH)
    @patch(QUICKBOOKS_CLIENT_PATH)
    def happy_path_qbm(self,
                       quickbooks_client_patch: Mock,
                       authclient_patch: Mock,
                       mock_auth_client: AuthClient,
                       mock_quickbooks_client: QuickBooks) -> QuickBooksModule:
        authclient_patch.return_value = mock_auth_client
        quickbooks_client_patch.return_value = mock_quickbooks_client
        return QuickBooksModule(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ENVIRONMENT, REFRESH_TOKEN, COMPANY_ID)

    @pytest.fixture
    def mock_qb_customer(self) -> Customer:
        return Mock(spec=Customer)

    @pytest.fixture
    def mock_qb_customer_list(self, mock_qb_customer: Customer) -> List[Customer]:
        return [mock_qb_customer for _ in SCHOOL_NAMES]

    @pytest.fixture
    def mock_school(self) -> School:
        return Mock(spec=School)

    @patch(CUSTOMER_CHOOSE_PATH)
    @patch(GET_SCHOOL_FROM_CUSTOMER_PATH)
    def test_query_schools_as_customers_happyPath(self,
                                                  get_school_from_customer_patch: Mock,
                                                  customer_choose_patch: Mock,
                                                  happy_path_qbm: QuickBooksModule,
                                                  mock_qb_customer_list: List[Customer],
                                                  mock_school: School,
                                                  mock_quickbooks_client: QuickBooks):
        # Setup
        customer_choose_patch.return_value = mock_qb_customer_list
        get_school_from_customer_patch.return_value = mock_school

        # Act
        schools = happy_path_qbm.query_schools_as_customers(SCHOOL_NAMES)

        # Verify
        assert schools == [mock_school for _ in SCHOOL_NAMES]
        customer_choose_patch.assert_called_once_with(SCHOOL_NAMES, DISPLAY_NAME, mock_quickbooks_client)
        get_school_from_customer_calls = [call(customer) for customer in mock_qb_customer_list]
        get_school_from_customer_patch.assert_has_calls(get_school_from_customer_calls)

    @patch(CUSTOMER_CHOOSE_PATH)
    def test_query_schools_as_customers_quickbooksRaises(self,
                                                         customer_choose_patch: Mock,
                                                         happy_path_qbm: QuickBooksModule,
                                                         mock_quickbooks_client: QuickBooks):
        # Setup
        customer_choose_patch.side_effect = QUICKBOOKS_EXCEPTION

        # Act
        try:
            schools = happy_path_qbm.query_schools_as_customers(SCHOOL_NAMES)
        except QuickbooksException as e:
            exn = e

        # Verify
        assert exn == QUICKBOOKS_EXCEPTION
        customer_choose_patch.assert_called_once_with(SCHOOL_NAMES, DISPLAY_NAME, mock_quickbooks_client)

    @patch(GET_CUSTOMER_FROM_SCHOOL_PATH)
    def test_create_customer_from_school_happyPath(self,
                                                   get_customer_from_school_patch: Mock,
                                                   mock_qb_customer: Customer,
                                                   happy_path_qbm: QuickBooksModule,
                                                   mock_school: School):
        # Setup
        get_customer_from_school_patch.return_value = mock_qb_customer

        # Act
        happy_path_qbm.create_customer_from_school(mock_school)

        # Verify
        get_customer_from_school_patch.assert_called_once_with(mock_school)
        mock_qb_customer.save.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)

    @patch(GET_CUSTOMER_FROM_SCHOOL_PATH)
    def test_create_customer_from_school_saveRaises(self,
                                                    get_customer_from_school_patch: Mock,
                                                    mock_qb_customer: Customer,
                                                    happy_path_qbm: QuickBooksModule,
                                                    mock_school: School):
        # Setup
        get_customer_from_school_patch.return_value = mock_qb_customer
        mock_qb_customer.save.side_effect = QUICKBOOKS_EXCEPTION

        # Act
        try:
            happy_path_qbm.create_customer_from_school(mock_school)
        except QuickbooksException as e:
            exn = e

        # Verify
        get_customer_from_school_patch.assert_called_once_with(mock_school)
        mock_qb_customer.save.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)
        assert exn == QUICKBOOKS_EXCEPTION

    @patch(GET_CUSTOMER_FROM_SCHOOL_PATH)
    def test_update_customer_from_school_happyPath(self,
                                                   get_customer_from_school_patch: Mock,
                                                   mock_qb_customer: Customer,
                                                   happy_path_qbm: QuickBooksModule,
                                                   mock_school: School):
        # Setup
        get_customer_from_school_patch.return_value = mock_qb_customer

        # Act
        happy_path_qbm.update_customer_from_school(CUSTOMER_ID, mock_school)

        # Verify
        get_customer_from_school_patch.assert_called_once_with(mock_school)
        assert mock_qb_customer.Id == CUSTOMER_ID
        mock_qb_customer.save.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)

    @patch(GET_CUSTOMER_FROM_SCHOOL_PATH)
    def test_update_customer_from_school_saveRaises(self,
                                                    get_customer_from_school_patch: Mock,
                                                    mock_qb_customer: Customer,
                                                    happy_path_qbm: QuickBooksModule,
                                                    mock_school: School):
        # Setup
        get_customer_from_school_patch.return_value = mock_qb_customer
        mock_qb_customer.save.side_effect = QUICKBOOKS_EXCEPTION

        # Act
        try:
            happy_path_qbm.update_customer_from_school(CUSTOMER_ID, mock_school)
        except QuickbooksException as e:
            exn = e

        # Verify
        get_customer_from_school_patch.assert_called_once_with(mock_school)
        assert mock_qb_customer.Id == CUSTOMER_ID
        mock_qb_customer.save.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)
        assert exn == QUICKBOOKS_EXCEPTION

