import datetime
from typing import List

import quickbooks.objects
from quickbooks.objects import Customer, PhoneNumber, EmailAddress, Invoice, Ref, SalesItemLine, SalesItemLineDetail, \
    Item

from invoice_automation.src.model.address import Address
from invoice_automation.src.model.conference import Conference
from invoice_automation.src.model.fee_type import FeeType
from invoice_automation.src.model.reg_round import RegRound
from invoice_automation.src.model.school import School

DELEGATE_FEE_TEMPLATE = "{} Delegate Fee"
SCHOOL_FEE_TEMPLATE = "{} School Fee"

CONFERENCE_TO_LINE_ITEM_NAMES = {
    Conference.BMUN71: [
        DELEGATE_FEE_TEMPLATE.format(Conference.BMUN71.value), SCHOOL_FEE_TEMPLATE.format(Conference.BMUN71.value)
    ],
    Conference.FC: [
        DELEGATE_FEE_TEMPLATE.format(Conference.FC.value), SCHOOL_FEE_TEMPLATE.format(Conference.FC.value)
    ],
    Conference.TEST: [
        DELEGATE_FEE_TEMPLATE.format(Conference.TEST.value), SCHOOL_FEE_TEMPLATE.format(Conference.TEST.value)
    ]
}


def get_customer_from_school(school: School | None) -> Customer | None:
    """
    Converts School object to QuickBooks Customer object
    :param school: School object to convert
    :return: QuickBooks Customer object corresponding to passed School object,
             None if None is passed
    """
    if school is None:
        return None

    customer = Customer()

    customer.CompanyName = school.school_name
    customer.DisplayName = school.school_name

    if school.email is None:
        customer.PrimaryEmailAddr = None
    else:
        customer.PrimaryEmailAddr = EmailAddress()
        customer.PrimaryEmailAddr.Address = school.email

    if school.phone_numbers is not None:
        if len(school.phone_numbers) > 0:
            customer.PrimaryPhone = PhoneNumber()
            customer.PrimaryPhone.FreeFormNumber = school.phone_numbers[0]
        if len(school.phone_numbers) > 1:
            customer.AlternatePhone = PhoneNumber()
            customer.AlternatePhone.FreeFormNumber = school.phone_numbers[1]

    customer.BillAddr = get_quickbooks_address_from_address(school.address)
    customer.ShipAddr = customer.BillAddr

    return customer


def get_school_from_customer(customer: Customer | None) -> School | None:
    """
    Converts QuickBooks Customer object to School object
    :param customer: QuickBooks Customer object to parse
    :return: Converted School object, None if None is passed
    """
    if customer is None:
        return None

    phone_numbers = []
    if customer.PrimaryPhone is not None:
        phone_numbers.append(customer.PrimaryPhone.FreeFormNumber)
    if customer.AlternatePhone is not None:
        phone_numbers.append(customer.AlternatePhone.FreeFormNumber)

    school = School(
        school_name=customer.DisplayName,
        email=customer.PrimaryEmailAddr.Address,
        phone_numbers=phone_numbers,
        address=get_address_from_quickbooks_address(customer.BillAddr)
    )
    school.id = customer.Id
    return school


def get_quickbooks_address_from_address(address: Address | None) -> quickbooks.objects.Address | None:
    """
    Converts Address object to QuickBooks Address object
    :param address: Address object to parse
    :return: Converted QuickBooks Address object, None if None is passed
    """
    if address is None:
        return None

    qbAddress = quickbooks.objects.Address()
    qbAddress.Line1 = address.line1
    qbAddress.Line2 = address.line2
    qbAddress.City = address.city
    qbAddress.CountrySubDivisionCode = address.country_sub_division_code
    qbAddress.Country = address.country
    qbAddress.PostalCode = address.zip_code

    return qbAddress


def get_address_from_quickbooks_address(address: quickbooks.objects.Address | None) -> Address | None:
    """
    Converts QuickBooks Address object to Address object
    :param address: QuickBooks Address object to parse
    :return: Converted Address object, None if None is passed
    """
    if address is None:
        return None

    return Address(
        address.Line1,
        address.Line2,
        address.City,
        address.CountrySubDivisionCode,
        address.Country,
        address.PostalCode
    )


def check_invoice_matches_items_and_counts(invoice: Invoice, item_names: List[str], item_counts: List[int]) -> bool:
    """
    Checks that the passed invoice match the passed items and counts
    Invoice should consist exactly of items with correct counts
    item_names[i] is expected to have count item_counts[i]
    Only SalesItemLines are checked from the invoice
    :param invoice:
    :param item_names:
    :param item_counts:
    :return:
    """
    if len(item_names) != len(item_counts):
        raise ValueError("item_refs and item_counts were expected to have the same length")

    line_items = list(filter(lambda i: i.DetailType == SALES_ITEM_LINE_DETAIL_TYPE, invoice.Line))
    if len(line_items) != len(item_names):
        return False

    invoice_item_counts = set()
    for item in line_items:
        invoice_item_name = item.SalesItemLineDetail.ItemRef.name
        # the item name in the invoice could have a category prepended
        if ":" in invoice_item_name:
            invoice_item_name = invoice_item_name.split(":")[1]
        invoice_item_count = item.SalesItemLineDetail.Qty
        invoice_item_counts.add((invoice_item_name, invoice_item_count))

    ref_item_counts = {item_count_tuple for item_count_tuple in zip(item_names, item_counts)}

    return invoice_item_counts == ref_item_counts


SALES_ITEM_LINE_DETAIL_TYPE = "SalesItemLineDetail"


SERVICE_DATES = {
    Conference.BMUN71: datetime.date(2023, 3, 5),
    Conference.FC: datetime.date(2022, 11, 12)
}


def create_SalesItemLine(item: Item, quantity: int, service_date: datetime.date) -> SalesItemLine:
    """
    Creates a SalesItemLine for use in an invoice
    :param item:
    :param quantity:
    :param service_date:
    :return:
    """
    line = SalesItemLine()
    line.Amount = int(quantity) * item.UnitPrice
    detail = SalesItemLineDetail()
    detail.ItemRef = item.to_ref()
    detail.Qty = quantity
    detail.UnitPrice = item.UnitPrice
    detail.ServiceDate = service_date.isoformat()
    line.SalesItemLineDetail = detail
    return line


END_DATES = {
    Conference.BMUN71: {
        RegRound.R1: datetime.date(2022, 10, 7),
        RegRound.R2: datetime.date(2022, 11, 4),
        RegRound.R3: datetime.date(2022, 12, 9),
        RegRound.R4: datetime.date(2023, 1, 6)
    },
    Conference.FC: {
        RegRound.R1: datetime.date(2022, 9, 16),
        RegRound.R2: datetime.date(2022, 10, 7)
    }
}


DUE_DATES = {
    Conference.BMUN71: {
        RegRound.R1: {
            FeeType.SCHOOL_FEE: datetime.date(2022, 10, 7),
            FeeType.DELEGATE_FEE: datetime.date(2022, 10, 28)
        },
        RegRound.R2: {
            FeeType.SCHOOL_FEE: datetime.date(2022, 11, 4),
            FeeType.DELEGATE_FEE: datetime.date(2022, 11, 25)
        },
        RegRound.R3: {
            FeeType.SCHOOL_FEE: datetime.date(2022, 12, 9),
            FeeType.DELEGATE_FEE: datetime.date(2023, 1, 6)
        },
        RegRound.R4: {
            FeeType.SCHOOL_FEE: datetime.date(2023, 1, 6),
            FeeType.DELEGATE_FEE: datetime.date(2023, 1, 27)
        }
    },
    Conference.FC: {
        RegRound.R1: {
            FeeType.SCHOOL_FEE: datetime.date(2022, 9, 16),
            FeeType.DELEGATE_FEE: datetime.date(2022, 9, 16)
        },
        RegRound.R2: {
            FeeType.SCHOOL_FEE: datetime.date(2022, 10, 7),
            FeeType.DELEGATE_FEE: datetime.date(2022, 10, 7)
        }
    }
}


def get_reg_round_from_conference_and_reg_time(conference: Conference, reg_date: datetime.datetime) -> RegRound:
    """
    Returns registration round based on conference and registration time
    :param conference:
    :param reg_date:
    :return:
    """
    for reg_round in END_DATES[conference]:
        if reg_date <= END_DATES[conference][reg_round]:
            return reg_round
    return RegRound.Late


def get_due_date_from_conference_fee_type_reg_time(
        reg_time: datetime.datetime,
        fee_type: FeeType,
        conference: Conference) -> datetime.date:
    reg_round = get_reg_round_from_conference_and_reg_time(conference, reg_time)
    return DUE_DATES[conference][reg_round][fee_type]
