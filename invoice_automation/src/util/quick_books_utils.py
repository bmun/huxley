import quickbooks.objects
from quickbooks.objects import Customer, PhoneNumber, EmailAddress

from invoice_automation.src.model.address import Address
from invoice_automation.src.model.school import School


def get_customer_from_school(school: School | None) -> Customer | None:
    """
    Converts School object to QuickBooks Customer object
    :param school: School object to convert
    :return: QuickBooks Customer object corresponding to passed School object,
             None if None is passed
    :raises: TypeError if School object is not passed
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
    :raises: TypeError if Customer object is not passed
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
    :raises: TypeError if Address object is not passed
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
    :raises: TypeError if QuickBooks Address object is not passed
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
