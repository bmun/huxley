from typing import List
from unittest.mock import Mock, patch

import pytest
import quickbooks.objects
from quickbooks.objects import Customer, EmailAddress, PhoneNumber, Invoice, DetailLine, SalesItemLineDetail, \
    SalesItemLine, Ref, Item

from huxley.invoice_automation.src.model.address import Address
from huxley.invoice_automation.src.model.school import School
from huxley.invoice_automation.src.util.quick_books_utils import get_customer_from_school, get_school_from_customer, \
    get_quickbooks_address_from_address, get_address_from_quickbooks_address, check_invoice_matches_items_and_counts, \
    create_SalesItemLine
from huxley.invoice_automation.tst.paths import GET_QUICKBOOKS_ADDRESS_FROM_ADDRESS_PATH, \
    GET_ADDRESS_FROM_QUICKBOOKS_ADDRESS_PATH

SCHOOL_NAME = "berkeley"
EMAIL = "carol@berkeley.edu"
PHONE_NUMBER1 = "call"
PHONE_NUMBER2 = "me"
CUSTOMER_ID = "id"
LINE1 = "Sather Tower"
LINE2 = "Floor 0"
CITY = "Berkeley"
COUNTRYSUBDIVISIONCODE = "CA"
COUNTRY = "USA"
POSTALCODE = "94720"
SCHOOL_FEE = "School Fee"
DELEGATE_FEE = "Delegate Fee"
DELEGATE_FEE_LINE_DETAIL_QTY = 20


def assert_qb_phone_number(p: PhoneNumber, expectedNumber: str):
    assert isinstance(p, PhoneNumber)
    assert p.FreeFormNumber == expectedNumber


def get_qb_PhoneNumber(freeFormNumber: str):
    phoneNumber = PhoneNumber()
    phoneNumber.FreeFormNumber = freeFormNumber
    return phoneNumber


class TestQuickbooksUtils:

    @pytest.fixture
    def mock_address(self) -> Address:
        return Mock(spec=Address)

    @pytest.fixture
    def mock_qb_address(self) -> quickbooks.objects.Address:
        return Mock(spec=quickbooks.objects.Address)

    @pytest.fixture
    def happy_path_school(self, mock_address) -> School:
        return School(
            school_name=SCHOOL_NAME,
            email=EMAIL,
            phone_numbers=[PHONE_NUMBER1, PHONE_NUMBER2],
            address=mock_address
        )

    @patch(GET_QUICKBOOKS_ADDRESS_FROM_ADDRESS_PATH)
    def test_get_customer_from_school_happyPath(self,
                                                mock_get_quickbooks_address_from_address: Mock,
                                                happy_path_school: School,
                                                mock_address: Address,
                                                mock_qb_address: quickbooks.objects.Address):
        # Setup
        mock_get_quickbooks_address_from_address.return_value = mock_qb_address

        # Act
        customer = get_customer_from_school(happy_path_school)

        # Verify
        assert customer.CompanyName == SCHOOL_NAME
        assert customer.DisplayName == SCHOOL_NAME
        assert isinstance(customer.PrimaryEmailAddr, EmailAddress)
        assert customer.PrimaryEmailAddr.Address == EMAIL
        assert_qb_phone_number(customer.PrimaryPhone, PHONE_NUMBER1)
        assert_qb_phone_number(customer.AlternatePhone, PHONE_NUMBER2)
        mock_get_quickbooks_address_from_address.assert_called_once_with(mock_address)
        assert customer.BillAddr == mock_qb_address
        assert customer.ShipAddr == mock_qb_address

    def test_get_customer_from_school_schoolIsNone(self):
        # Act
        customer = get_customer_from_school(None)

        # Verify
        assert customer is None

    @patch(GET_QUICKBOOKS_ADDRESS_FROM_ADDRESS_PATH)
    def test_get_customer_from_school_emailIsNone(self,
                                                  mock_get_quickbooks_address_from_address: Mock,
                                                  happy_path_school: School,
                                                  mock_address: Address,
                                                  mock_qb_address: quickbooks.objects.Address):
        # Setup
        happy_path_school.email = None
        mock_get_quickbooks_address_from_address.return_value = mock_qb_address

        # Act
        customer = get_customer_from_school(happy_path_school)

        # Verify
        assert customer.CompanyName == SCHOOL_NAME
        assert customer.DisplayName == SCHOOL_NAME
        assert customer.PrimaryEmailAddr is None
        assert_qb_phone_number(customer.PrimaryPhone, PHONE_NUMBER1)
        assert_qb_phone_number(customer.AlternatePhone, PHONE_NUMBER2)
        mock_get_quickbooks_address_from_address.assert_called_once_with(mock_address)
        assert customer.BillAddr == mock_qb_address
        assert customer.ShipAddr == mock_qb_address

    @pytest.fixture
    def happy_path_customer(self, mock_qb_address: quickbooks.objects.Address) -> Customer:
        customer = Customer()
        customer.DisplayName = SCHOOL_NAME
        customer.PrimaryEmailAddr = EmailAddress()
        customer.PrimaryEmailAddr.Address = EMAIL
        customer.PrimaryPhone = get_qb_PhoneNumber(PHONE_NUMBER1)
        customer.AlternatePhone = get_qb_PhoneNumber(PHONE_NUMBER2)
        customer.BillAddr = mock_qb_address
        customer.Id = CUSTOMER_ID
        return customer

    @patch(GET_ADDRESS_FROM_QUICKBOOKS_ADDRESS_PATH)
    def test_get_school_from_customer_happyPath(self,
                                                mock_get_address_from_quickbooks_address: Mock,
                                                happy_path_customer: Customer,
                                                mock_qb_address: quickbooks.objects.Address,
                                                mock_address: Address):
        # Setup
        mock_get_address_from_quickbooks_address.return_value = mock_address

        # Act
        school = get_school_from_customer(happy_path_customer)

        # Verify
        assert school.school_name == SCHOOL_NAME
        assert school.email == EMAIL
        assert school.phone_numbers == [PHONE_NUMBER1, PHONE_NUMBER2]
        mock_get_address_from_quickbooks_address.assert_called_once_with(mock_qb_address)
        assert school.address == mock_address
        assert school.id == CUSTOMER_ID

    def test_get_school_from_customer_customerIsNone(self):
        # Act
        school = get_school_from_customer(None)

        # Verify
        assert school is None

    @pytest.fixture
    def happy_path_address(self) -> Address:
        return Address(LINE1, LINE2, CITY, COUNTRYSUBDIVISIONCODE, COUNTRY, POSTALCODE)

    def test_get_quickbooks_address_from_address_happyPath(self, happy_path_address: Address):
        # Act
        qbAddress = get_quickbooks_address_from_address(happy_path_address)

        # Verify
        assert qbAddress.Line1 == LINE1
        assert qbAddress.Line2 == LINE2
        assert qbAddress.City == CITY
        assert qbAddress.CountrySubDivisionCode == COUNTRYSUBDIVISIONCODE
        assert qbAddress.Country == COUNTRY
        assert qbAddress.PostalCode == POSTALCODE

    def test_get_quickbooks_address_from_address_addressIsNone(self):
        # Act
        qbAddress = get_quickbooks_address_from_address(None)

        # Verify
        assert qbAddress is None

    @pytest.fixture
    def happy_path_qb_address(self) -> quickbooks.objects.Address:
        qbAddress = quickbooks.objects.Address()
        qbAddress.Line1 = LINE1
        qbAddress.Line2 = LINE2
        qbAddress.City = CITY
        qbAddress.CountrySubDivisionCode = COUNTRYSUBDIVISIONCODE
        qbAddress.Country = COUNTRY
        qbAddress.PostalCode = POSTALCODE
        return qbAddress

    def test_get_address_from_quickbooks_address_happyPath(self, happy_path_qb_address: quickbooks.objects.Address):
        # Act
        address = get_address_from_quickbooks_address(happy_path_qb_address)

        # Verify
        assert address.line1 == LINE1
        assert address.line2 == LINE2
        assert address.city == CITY
        assert address.country_sub_division_code == COUNTRYSUBDIVISIONCODE
        assert address.country == COUNTRY
        assert address.zip_code == POSTALCODE

    def test_get_address_from_quickbooks_address_qbAddressIsNone(self,
                                                                 happy_path_qb_address: quickbooks.objects.Address):
        # Act
        address = get_address_from_quickbooks_address(None)

        # Verify
        assert address is None

    @pytest.fixture
    def mock_school_fee_salesitemline(self) -> SalesItemLine:
        detail = Mock(spec=SalesItemLineDetail)
        detail.ItemRef = Ref()
        detail.ItemRef.name = SCHOOL_FEE
        detail.Qty = 1
        line = SalesItemLine()
        line.SalesItemLineDetail = detail
        return line

    @pytest.fixture
    def mock_delegate_fee_salesitemline(self) -> SalesItemLine:
        detail = Mock(spec=SalesItemLineDetail)
        detail.ItemRef = Ref()
        detail.ItemRef.name = DELEGATE_FEE
        detail.Qty = DELEGATE_FEE_LINE_DETAIL_QTY
        line = SalesItemLine()
        line.SalesItemLineDetail = detail
        return line

    @pytest.fixture
    def mock_line(self,
                  mock_school_fee_salesitemline: SalesItemLine,
                  mock_delegate_fee_salesitemline: SalesItemLine) -> List[DetailLine]:
        return [mock_school_fee_salesitemline, mock_delegate_fee_salesitemline]

    @pytest.fixture
    def mock_invoice(self, mock_line: List[DetailLine]) -> Invoice:
        invoice = Mock(spec=Invoice)
        invoice.Line = mock_line
        return invoice

    def test_check_invoice_matches_items_and_counts_happyPath(self,
                                                              mock_invoice: Invoice):
        # Act
        invoice_matches = check_invoice_matches_items_and_counts(
            mock_invoice,
            [SCHOOL_FEE, DELEGATE_FEE],
            [1, DELEGATE_FEE_LINE_DETAIL_QTY]
        )

        # Verify
        assert invoice_matches is True

    def test_check_invoice_matches_items_and_counts_itemCountLengthMismatch(self,
                                                                            mock_invoice: Invoice):
        # Act
        try:
            invoice_matches = check_invoice_matches_items_and_counts(
                mock_invoice,
                [SCHOOL_FEE, DELEGATE_FEE],
                [1]
            )
        except ValueError as e:
            exn = e

        # Verify
        assert str(exn) == "item_refs and item_counts were expected to have the same length"

    def test_check_invoice_matches_items_and_counts_nonMatchingInvoice(self,
                                                                       mock_invoice: Invoice,
                                                                       mock_school_fee_salesitemline: SalesItemLine,
                                                                       mock_delegate_fee_salesitemline: SalesItemLine):
        # Act
        invoice_matches = check_invoice_matches_items_and_counts(
            mock_invoice,
            [SCHOOL_FEE],
            [1]
        )

        # Verify
        assert invoice_matches is False

    @pytest.fixture
    def mock_item(self) -> Item:
        return Mock(spec=Item)

    @pytest.fixture
    def mock_item_ref(self) -> Ref:
        return Mock(spec=Ref)

    def test_create_SalesItemLine_happyPath(self,
                                  mock_item: Item,
                                  mock_item_ref: Ref):
        unit_price = 85
        quantity = 20
        # Setup
        mock_item.UnitPrice = unit_price
        mock_item.to_ref.return_value = mock_item_ref

        # Act
        line = create_SalesItemLine(mock_item, quantity)

        # Verify
        assert isinstance(line, SalesItemLine)
        assert line.Amount == unit_price * quantity
        detail = line.SalesItemLineDetail
        assert isinstance(detail, SalesItemLineDetail)
        assert detail.ItemRef == mock_item_ref
        assert detail.Qty == quantity
        assert detail.UnitPrice == unit_price
