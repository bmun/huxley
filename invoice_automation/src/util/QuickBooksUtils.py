import quickbooks.objects
from quickbooks.objects import Customer, PhoneNumber, EmailAddress

from invoice_automation.src.model.Address import Address
from invoice_automation.src.model.School import School


def getCustomerFromSchool(school: School) -> Customer | None:
    """
    Converts School object to QuickBooks Customer object
    :param school: School object to convert
    :return: QuickBooks Customer object corresponding to passed School object,
             None if None is passed
    :raises: TypeError if School object is not passed
    """
    if school is None:
        return None
    if not isinstance(school, School):
        raise TypeError(f"Expected a School object, was {type(school)}")

    customer = Customer()

    customer.CompanyName = school.schoolName
    customer.DisplayName = school.schoolName

    if school.email is None:
        customer.PrimaryEmailAddr = None
    else:
        customer.PrimaryEmailAddr = EmailAddress()
        customer.PrimaryEmailAddr.Address = school.email

    if school.phoneNumbers is not None:
        if len(school.phoneNumbers) > 0:
            customer.PrimaryPhone = PhoneNumber()
            customer.PrimaryPhone.FreeFormNumber = school.phoneNumbers[0]
        if len(school.phoneNumbers) > 1:
            customer.AlternatePhone = PhoneNumber()
            customer.AlternatePhone.FreeFormNumber = school.phoneNumbers[1]

    customer.BillAddr = getQuickBooksAddressFromAddress(school.address)

    return customer


def getSchoolFromCustomer(customer: Customer) -> School | None:
    """
    Converts QuickBooks Customer object to School object
    :param customer: QuickBooks Customer object to parse
    :return: Converted School object, None if None is passed
    :raises: TypeError if Customer object is not passed
    """
    if customer is None:
        return None
    if not isinstance(customer, Customer):
        raise TypeError(f"Expected a Customer object, was {type(customer)}")

    school = School(
        schoolName=customer.DisplayName,
        email=customer.PrimaryEmailAddr,
        phoneNumbers=[customer.PrimaryPhone, customer.AlternatePhone],
        address=getAddressFromQuickBooksAddress(customer.BillAddr)
    )
    school.id = customer.Id
    return school


def getQuickBooksAddressFromAddress(address: Address) -> quickbooks.objects.Address | None:
    """
    Converts Address object to QuickBooks Address object
    :param address: Address object to parse
    :return: Converted QuickBooks Address object, None if None is passed
    :raises: TypeError if Address object is not passed
    """
    if address is None:
        return None
    if not isinstance(address, Address):
        raise TypeError(f"Expected an Address object, was {type(address)}")

    qbAddress = quickbooks.objects.Address()
    qbAddress.Line1 = address.line1
    qbAddress.Line2 = address.line2
    qbAddress.City = address.city
    qbAddress.CountrySubDivisionCode = address.countrySubDivisionCode
    qbAddress.Country = address.country
    qbAddress.PostalCode = address.zipCode

    return qbAddress


def getAddressFromQuickBooksAddress(address: quickbooks.objects.Address) -> Address | None:
    """
    Converts QuickBooks Address object to Address object
    :param address: QuickBooks Address object to parse
    :return: Converted Address object, None if None is passed
    :raises: TypeError if QuickBooks Address object is not passed
    """
    if address is None:
        return None
    if not isinstance(address, quickbooks.objects.Address):
        raise TypeError(f"Expected a QuickBooks Address object, was {type(address)}")

    return Address(
        address.Line1,
        address.Line2,
        address.City,
        address.CountrySubDivisionCode,
        address.Country,
        address.PostalCode
    )
