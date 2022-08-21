from unittest.mock import Mock, patch

import pytest
import quickbooks.objects
from quickbooks.objects import Customer, EmailAddress, PhoneNumber

from invoice_automation.src.model.address import Address
from invoice_automation.src.model.school import School
from invoice_automation.src.util.quick_books_utils import get_customer_from_school, get_school_from_customer, \
    get_quickbooks_address_from_address, get_address_from_quickbooks_address
from invoice_automation.tst.paths import GET_QUICKBOOKS_ADDRESS_FROM_ADDRESS_PATH, \
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
