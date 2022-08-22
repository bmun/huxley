from typing import List, Callable
from unittest.mock import patch, Mock, call, MagicMock

import pytest
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Customer, Ref, Invoice, Item, SalesItemLine

import invoice_automation.src.module.quick_books_module
from invoice_automation.src.model.conference import Conference
from invoice_automation.src.model.registration import Registration
from invoice_automation.src.model.school import School
from invoice_automation.src.module.quick_books_module import QuickBooksModule, DISPLAY_NAME
from invoice_automation.tst.paths import AUTHCLIENT_PATH, QUICKBOOKS_CLIENT_PATH, CUSTOMER_CHOOSE_PATH, \
    GET_SCHOOL_FROM_CUSTOMER_PATH, GET_CUSTOMER_FROM_SCHOOL_PATH, CONFERENCE_TO_LINE_ITEM_NAMES_PATH, ITEM_CHOOSE_PATH, \
    INVOICE_QUERY_PATH, CONSTRUCT_INVOICE_QUERY_PATH, GET_CUSTOMER_REF_FROM_SCHOOL, QUERY_INVOICES_FROM_CUSTOMER_REF, \
    CHECK_INVOICE_MATCHES_ITEMS_AND_COUNTS_PATH, QUERY_LINE_ITEMS_FROM_CONFERENCE, CREATE_SALESITEMLINE_PATH, \
    INVOICE_PATH

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
CUSTOMER_NAME = "Sora"
NUM_DELEGATES = 20
TEST_DELEGATE_FEE = "Test Delegate Fee"
TEST_SCHOOL_FEE = "Test School Fee"


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

    @pytest.fixture
    def mock_customer_ref(self) -> Ref:
        mock_ref = Mock(spec=Ref)
        mock_ref.type = "Customer"
        return mock_ref

    @patch(CUSTOMER_CHOOSE_PATH)
    def test_get_customer_ref_from_school_happyPath(self,
                                                    customer_choose_patch: Mock,
                                                    mock_qb_customer: Customer,
                                                    mock_customer_ref: Ref,
                                                    happy_path_qbm: QuickBooksModule,
                                                    mock_school: School):
        # Setup
        customer_choose_patch.return_value = [mock_qb_customer]
        mock_qb_customer.to_ref.return_value = mock_customer_ref
        mock_school.school_name = SCHOOL_NAMES[0]

        # Act
        customer_ref = happy_path_qbm.get_customer_ref_from_school(mock_school)

        # Verify
        assert customer_ref == mock_customer_ref
        customer_choose_patch.assert_called_once_with(
            [SCHOOL_NAMES[0]],
            field="DisplayName",
            qb=happy_path_qbm.quickbooks_client
        )
        mock_qb_customer.to_ref.assert_called_once()

    def test_get_customer_ref_from_school_schoolIsNone(self, happy_path_qbm: QuickBooksModule):
        # Act
        customer_ref = happy_path_qbm.get_customer_ref_from_school(None)

        # Verify
        assert customer_ref is None

    @patch(CUSTOMER_CHOOSE_PATH)
    def test_get_customer_ref_from_school_customerChooseRaises(self,
                                                               customer_choose_patch: Mock,
                                                               happy_path_qbm: QuickBooksModule,
                                                               mock_school: School):
        # Setup
        customer_choose_patch.side_effect = QUICKBOOKS_EXCEPTION
        mock_school.school_name = SCHOOL_NAMES[0]

        # Act
        try:
            customer_ref = happy_path_qbm.get_customer_ref_from_school(mock_school)
        except QuickbooksException as e:
            exn = e

        # Verify
        assert exn == QUICKBOOKS_EXCEPTION
        customer_choose_patch.assert_called_once_with(
            [SCHOOL_NAMES[0]],
            field="DisplayName",
            qb=happy_path_qbm.quickbooks_client
        )

    @patch(CUSTOMER_CHOOSE_PATH)
    def test_get_customer_ref_from_school_noMatchingCustomers(self,
                                                              customer_choose_patch: Mock,
                                                              happy_path_qbm: QuickBooksModule,
                                                              mock_school: School):
        # Setup
        customer_choose_patch.return_value = []
        mock_school.school_name = SCHOOL_NAMES[0]

        # Act
        customer_ref = happy_path_qbm.get_customer_ref_from_school(mock_school)

        # Verify
        assert customer_ref is None
        customer_choose_patch.assert_called_once_with(
            [SCHOOL_NAMES[0]],
            field="DisplayName",
            qb=happy_path_qbm.quickbooks_client
        )

    @pytest.fixture
    def mock_item_names(self) -> List:
        return Mock(spec=List)

    @pytest.fixture
    def mock_item_list(self) -> List:
        return Mock(spec=List)

    @pytest.fixture
    def mock_conference(self) -> Conference:
        return Mock(spec=Conference)

    @patch(CONFERENCE_TO_LINE_ITEM_NAMES_PATH)
    @patch(ITEM_CHOOSE_PATH)
    def test_query_line_item_from_conference_happyPath(self,
                                                       item_choose_patch: Mock,
                                                       conference_to_line_item_names_patch: Mock,
                                                       mock_item_names: List,
                                                       mock_item_list: List,
                                                       happy_path_qbm: QuickBooksModule,
                                                       mock_conference: Conference):
        # Setup
        conference_to_line_item_names_patch.__getitem__.return_value = mock_item_names
        item_choose_patch.return_value = mock_item_list

        # Act
        item_list = happy_path_qbm.query_line_items_from_conference(mock_conference)

        # Verify
        assert item_list == mock_item_list
        conference_to_line_item_names_patch.__getitem__.assert_called_once()
        item_choose_patch.assert_called_once_with(mock_item_names, field="Name", qb=happy_path_qbm.quickbooks_client)

    @patch(CONFERENCE_TO_LINE_ITEM_NAMES_PATH)
    @patch(ITEM_CHOOSE_PATH)
    def test_query_line_item_from_conference_chooseRaises(self,
                                                          item_choose_patch: Mock,
                                                          conference_to_line_item_names_patch: Mock,
                                                          mock_item_names: List,
                                                          happy_path_qbm: QuickBooksModule,
                                                          mock_conference: Conference):
        # Setup
        conference_to_line_item_names_patch.__getitem__.return_value = mock_item_names
        item_choose_patch.side_effect = QUICKBOOKS_EXCEPTION

        # Act
        try:
            item_list = happy_path_qbm.query_line_items_from_conference(mock_conference)
        except QuickbooksException as e:
            exn = e

        # Verify
        assert exn == QUICKBOOKS_EXCEPTION
        conference_to_line_item_names_patch.__getitem__.assert_called_once()
        item_choose_patch.assert_called_once_with(mock_item_names, field="Name", qb=happy_path_qbm.quickbooks_client)

    @pytest.fixture
    def mock_non_empty_invoice_list(self) -> List[Invoice]:
        lst = MagicMock()
        lst.__len__.return_value = 3
        return lst

    @pytest.fixture
    def mock_invoice_query(self) -> str:
        return Mock(spec=str)

    @patch(INVOICE_QUERY_PATH)
    @patch(CONSTRUCT_INVOICE_QUERY_PATH)
    def test_query_invoices_from_customer_ref_happyPath(self,
                                                        construct_invoice_query_patch: Mock,
                                                        invoice_query_patch: Mock,
                                                        mock_invoice_query: str,
                                                        mock_customer_ref: Ref,
                                                        mock_non_empty_invoice_list: List,
                                                        happy_path_qbm: QuickBooksModule):
        # Setup
        construct_invoice_query_patch.return_value = mock_invoice_query
        invoice_query_patch.return_value = mock_non_empty_invoice_list

        # Act
        invoices = happy_path_qbm.query_invoices_from_customer_ref(mock_customer_ref)

        # Verify
        assert invoices == mock_non_empty_invoice_list
        invoice_query_patch.assert_called_once_with(mock_invoice_query, qb=happy_path_qbm.quickbooks_client)

    @patch(INVOICE_QUERY_PATH)
    @patch(CONSTRUCT_INVOICE_QUERY_PATH)
    def test_query_invoices_from_customer_ref_noInvoicesFound(self,
                                                              construct_invoice_query_patch: Mock,
                                                              invoice_query_patch: Mock,
                                                              mock_invoice_query: str,
                                                              mock_customer_ref: Ref,
                                                              happy_path_qbm: QuickBooksModule):
        # Setup
        construct_invoice_query_patch.return_value = mock_invoice_query
        invoice_query_patch.return_value = []

        # Act
        invoices = happy_path_qbm.query_invoices_from_customer_ref(mock_customer_ref)

        # Verify
        assert invoices is None
        invoice_query_patch.assert_called_once_with(mock_invoice_query, qb=happy_path_qbm.quickbooks_client)

    @patch(INVOICE_QUERY_PATH)
    @patch(CONSTRUCT_INVOICE_QUERY_PATH)
    def test_query_invoices_from_customer_ref_invoiceQueryRaises(self,
                                                                 construct_invoice_query_patch: Mock,
                                                                 invoice_query_patch: Mock,
                                                                 mock_invoice_query: str,
                                                                 mock_customer_ref: Ref,
                                                                 happy_path_qbm: QuickBooksModule):
        # Setup
        construct_invoice_query_patch.return_value = mock_invoice_query
        invoice_query_patch.side_effect = QUICKBOOKS_EXCEPTION

        # Act
        try:
            invoices = happy_path_qbm.query_invoices_from_customer_ref(mock_customer_ref)
        except QuickbooksException as e:
            exn = e

        # Verify
        assert exn == QUICKBOOKS_EXCEPTION
        invoice_query_patch.assert_called_once_with(mock_invoice_query, qb=happy_path_qbm.quickbooks_client)

    @pytest.fixture
    def happy_path_school(self) -> School:
        return School(SCHOOL_NAMES[0])

    @pytest.fixture
    def happy_path_registration(self, happy_path_school: School) -> Registration:
        return Registration(happy_path_school, NUM_DELEGATES, Conference.TEST)

    @pytest.fixture
    def happy_path_customer_ref(self) -> Ref:
        ref = Ref()
        ref.name = SCHOOL_NAMES[0]
        ref.type = "Customer"
        return ref

    @pytest.fixture
    def happy_path_mock_matching_invoice(self) -> Invoice:
        return Mock(spec=Invoice)

    @pytest.fixture
    def happy_path_mock_non_matching_invoice(self) -> Invoice:
        return Mock(spec=Invoice)

    @pytest.fixture
    def happy_path_invoices(self,
                            happy_path_mock_matching_invoice: Invoice,
                            happy_path_mock_non_matching_invoice: Invoice) -> List[Invoice]:
        return [happy_path_mock_non_matching_invoice, happy_path_mock_matching_invoice]

    @pytest.fixture
    def check_invoice_matches_items_and_counts_replacement(
            self,
            happy_path_mock_matching_invoice: Invoice
    ) -> Callable[[Invoice, List, List], bool]:
        def side_effect(invoice: Invoice, item_names, item_counts):
            if invoice == happy_path_mock_matching_invoice:
                return True
            else:
                return False
        return side_effect

    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, GET_CUSTOMER_REF_FROM_SCHOOL)
    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, QUERY_INVOICES_FROM_CUSTOMER_REF)
    @patch(CHECK_INVOICE_MATCHES_ITEMS_AND_COUNTS_PATH)
    def test_check_invoice_matches_items_and_counts_happyPath(
            self,
            check_invoice_matches_items_and_counts_patch: Mock,
            query_invoices_from_customer_ref_patch: Mock,
            get_customer_ref_from_school_patch: Mock,
            happy_path_customer_ref: Ref,
            happy_path_invoices: List[Invoice],
            check_invoice_matches_items_and_counts_replacement: Callable[[Invoice, List, List], bool],
            happy_path_qbm: QuickBooksModule,
            happy_path_registration: Registration,
            happy_path_mock_matching_invoice: Invoice,
            happy_path_mock_non_matching_invoice: Invoice,
            happy_path_school: School
    ):
        # Setup
        get_customer_ref_from_school_patch.return_value = happy_path_customer_ref
        query_invoices_from_customer_ref_patch.return_value = happy_path_invoices
        check_invoice_matches_items_and_counts_patch.side_effect = check_invoice_matches_items_and_counts_replacement

        # Act
        invoice = happy_path_qbm.query_invoice_from_registration(happy_path_registration)

        # Verify
        assert invoice == happy_path_mock_matching_invoice
        get_customer_ref_from_school_patch.assert_called_once_with(happy_path_school)
        query_invoices_from_customer_ref_patch.assert_called_once_with(happy_path_customer_ref)
        expected_item_names = [TEST_DELEGATE_FEE, TEST_SCHOOL_FEE]
        expected_item_counts = [NUM_DELEGATES, 1]
        expected_check_invoice_matches_calls = [
            call(happy_path_mock_non_matching_invoice, expected_item_names, expected_item_counts),
            call(happy_path_mock_matching_invoice, expected_item_names, expected_item_counts)
        ]
        check_invoice_matches_items_and_counts_patch.assert_has_calls(expected_check_invoice_matches_calls)

    def test_check_invoice_matches_items_and_counts_registrationIsNone(self, happy_path_qbm: QuickBooksModule):
        # Act
        invoice = happy_path_qbm.query_invoice_from_registration(None)

        # Verify
        assert invoice is None

    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, GET_CUSTOMER_REF_FROM_SCHOOL)
    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, QUERY_INVOICES_FROM_CUSTOMER_REF)
    def test_check_invoice_matches_items_and_counts_noInvoicesReturned(
            self,
            query_invoices_from_customer_ref_patch: Mock,
            get_customer_ref_from_school_patch: Mock,
            happy_path_qbm: QuickBooksModule,
            happy_path_customer_ref: Ref,
            happy_path_registration: Registration,
            happy_path_school: School
    ):
        # Setup
        get_customer_ref_from_school_patch.return_value = happy_path_customer_ref
        query_invoices_from_customer_ref_patch.return_value = None

        # Act
        invoice = happy_path_qbm.query_invoice_from_registration(happy_path_registration)

        # Verify
        assert invoice is None
        get_customer_ref_from_school_patch.assert_called_once_with(happy_path_school)
        query_invoices_from_customer_ref_patch.assert_called_once_with(happy_path_customer_ref)

    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, GET_CUSTOMER_REF_FROM_SCHOOL)
    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, QUERY_INVOICES_FROM_CUSTOMER_REF)
    @patch(CHECK_INVOICE_MATCHES_ITEMS_AND_COUNTS_PATH)
    def test_check_invoice_matches_items_and_counts_noMatchingInvoices(
            self,
            check_invoice_matches_items_and_counts_patch: Mock,
            query_invoices_from_customer_ref_patch: Mock,
            get_customer_ref_from_school_patch: Mock,
            happy_path_customer_ref: Ref,
            happy_path_invoices: List[Invoice],
            happy_path_qbm: QuickBooksModule,
            happy_path_registration: Registration,
            happy_path_mock_matching_invoice: Invoice,
            happy_path_mock_non_matching_invoice: Invoice,
            happy_path_school: School
    ):
        # Setup
        get_customer_ref_from_school_patch.return_value = happy_path_customer_ref
        query_invoices_from_customer_ref_patch.return_value = happy_path_invoices
        check_invoice_matches_items_and_counts_patch.side_effect = lambda i, i_n, i_c: False

        # Act
        invoice = happy_path_qbm.query_invoice_from_registration(happy_path_registration)

        # Verify
        assert invoice is None
        get_customer_ref_from_school_patch.assert_called_once_with(happy_path_school)
        query_invoices_from_customer_ref_patch.assert_called_once_with(happy_path_customer_ref)
        expected_item_names = [TEST_DELEGATE_FEE, TEST_SCHOOL_FEE]
        expected_item_counts = [NUM_DELEGATES, 1]
        expected_check_invoice_matches_calls = [
            call(happy_path_mock_non_matching_invoice, expected_item_names, expected_item_counts),
            call(happy_path_mock_matching_invoice, expected_item_names, expected_item_counts)
        ]
        check_invoice_matches_items_and_counts_patch.assert_has_calls(expected_check_invoice_matches_calls)

    @pytest.fixture
    def mock_school_fee_item(self) -> Item:
        item = Mock(spec=Item)
        item.Name = TEST_SCHOOL_FEE
        return item

    @pytest.fixture
    def mock_delegate_fee_item(self) -> Item:
        item = Mock(spec=Item)
        item.Name = TEST_DELEGATE_FEE
        return item

    @pytest.fixture
    def mock_school_fee_SalesItemLine(self) -> SalesItemLine:
        return Mock(spec=SalesItemLine)

    @pytest.fixture
    def mock_delegate_fee_SalesItemLine(self) -> SalesItemLine:
        return Mock(spec=SalesItemLine)

    @pytest.fixture
    def create_SalesItemLine_sideEffect(
            self,
            mock_school_fee_SalesItemLine: SalesItemLine,
            mock_delegate_fee_SalesItemLine: SalesItemLine,
            mock_school_fee_item: Item,
            mock_delegate_fee_item: Item) -> Callable[[Item, int], SalesItemLine]:
        def create_SalesItemLine(item: Item, quantity: int):
            if item == mock_school_fee_item:
                return mock_school_fee_SalesItemLine
            elif item == mock_delegate_fee_item:
                return mock_delegate_fee_SalesItemLine
        return create_SalesItemLine

    @pytest.fixture
    def mock_invoice(self) -> Invoice:
        return Mock(spec=Invoice)

    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, GET_CUSTOMER_REF_FROM_SCHOOL)
    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, QUERY_LINE_ITEMS_FROM_CONFERENCE)
    @patch(CREATE_SALESITEMLINE_PATH)
    @patch(INVOICE_PATH)
    def test_create_invoice_from_registration_happyPath(self,
                                                        invoice_patch: Mock,
                                                        create_SalesItemLine_patch: Mock,
                                                        query_line_items_from_conference_patch: Mock,
                                                        get_customer_ref_from_school_patch: Mock,
                                                        mock_customer_ref: Ref,
                                                        mock_school_fee_item: Item,
                                                        mock_delegate_fee_item: Item,
                                                        create_SalesItemLine_sideEffect: Callable[[Item, int], SalesItemLine],
                                                        mock_invoice: Invoice,
                                                        happy_path_qbm: QuickBooksModule,
                                                        happy_path_registration: Registration,
                                                        mock_school_fee_SalesItemLine: SalesItemLine,
                                                        mock_delegate_fee_SalesItemLine: SalesItemLine):
        # Setup
        get_customer_ref_from_school_patch.return_value = mock_customer_ref
        query_line_items_from_conference_patch.return_value = [mock_school_fee_item, mock_delegate_fee_item]
        create_SalesItemLine_patch.side_effect = create_SalesItemLine_sideEffect
        invoice_patch.return_value = mock_invoice
        mock_invoice.save.return_value = None

        # Act
        happy_path_qbm.create_invoice_from_registration(happy_path_registration, "")

        # Verify
        get_customer_ref_from_school_patch.assert_called_once_with(happy_path_registration.school)
        query_line_items_from_conference_patch.assert_called_once_with(happy_path_registration.conference)
        create_SalesItemLine_calls = [call(mock_school_fee_item, 1), call(mock_delegate_fee_item, NUM_DELEGATES)]
        create_SalesItemLine_patch.assert_has_calls(create_SalesItemLine_calls)
        assert mock_invoice.CustomerRef == mock_customer_ref
        assert mock_invoice.Line == [mock_school_fee_SalesItemLine, mock_delegate_fee_SalesItemLine]
        mock_invoice.save.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)

    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, GET_CUSTOMER_REF_FROM_SCHOOL)
    @patch.object(invoice_automation.src.module.quick_books_module.QuickBooksModule, QUERY_LINE_ITEMS_FROM_CONFERENCE)
    @patch(CREATE_SALESITEMLINE_PATH)
    @patch(INVOICE_PATH)
    def test_create_invoice_from_registration_saveRaises(self,
                                                        invoice_patch: Mock,
                                                        create_SalesItemLine_patch: Mock,
                                                        query_line_items_from_conference_patch: Mock,
                                                        get_customer_ref_from_school_patch: Mock,
                                                        mock_customer_ref: Ref,
                                                        mock_school_fee_item: Item,
                                                        mock_delegate_fee_item: Item,
                                                        create_SalesItemLine_sideEffect: Callable[[Item, int], SalesItemLine],
                                                        mock_invoice: Invoice,
                                                        happy_path_qbm: QuickBooksModule,
                                                        happy_path_registration: Registration,
                                                        mock_school_fee_SalesItemLine: SalesItemLine,
                                                        mock_delegate_fee_SalesItemLine: SalesItemLine):
        # Setup
        get_customer_ref_from_school_patch.return_value = mock_customer_ref
        query_line_items_from_conference_patch.return_value = [mock_school_fee_item, mock_delegate_fee_item]
        create_SalesItemLine_patch.side_effect = create_SalesItemLine_sideEffect
        invoice_patch.return_value = mock_invoice
        mock_invoice.save.side_effect = QUICKBOOKS_EXCEPTION

        # Act
        try:
            happy_path_qbm.create_invoice_from_registration(happy_path_registration, "")
        except QuickbooksException as e:
            exn = e

        # Verify
        assert exn == QUICKBOOKS_EXCEPTION
        get_customer_ref_from_school_patch.assert_called_once_with(happy_path_registration.school)
        query_line_items_from_conference_patch.assert_called_once_with(happy_path_registration.conference)
        create_SalesItemLine_calls = [call(mock_school_fee_item, 1), call(mock_delegate_fee_item, NUM_DELEGATES)]
        create_SalesItemLine_patch.assert_has_calls(create_SalesItemLine_calls)
        assert mock_invoice.CustomerRef == mock_customer_ref
        assert mock_invoice.Line == [mock_school_fee_SalesItemLine, mock_delegate_fee_SalesItemLine]
        mock_invoice.save.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)

    def test_send_invoice_happyPath(self, mock_invoice: Invoice, happy_path_qbm: QuickBooksModule):
        # Setup
        mock_invoice.send.return_value = None

        # Act
        happy_path_qbm.send_invoice(mock_invoice)

        # Verify
        mock_invoice.send.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)

    def test_send_invoice_sendRaises(self, mock_invoice: Invoice, happy_path_qbm: QuickBooksModule):
        # Setup
        mock_invoice.send.side_effect = QUICKBOOKS_EXCEPTION

        # Act
        try:
            happy_path_qbm.send_invoice(mock_invoice)
        except QuickbooksException as e:
            exn = e

        # Verify
        assert exn == QUICKBOOKS_EXCEPTION
        mock_invoice.send.assert_called_once_with(qb=happy_path_qbm.quickbooks_client)
