import quickbooks.objects
from quickbooks.objects import Customer, PhoneNumber

from invoice_automation.src.model.Address import Address
from invoice_automation.src.model.School import School


def getCustomerFromSchool(school: School) -> Customer:
    if school is None:
        return None
    if not isinstance(school, School):
        raise TypeError(f"Expected a School object, was {type(school)}")

    customer = Customer()
    customer.CompanyName = school.schoolName
    customer.PrimaryEmailAddr = school.email
    if len(school.phoneNumbers) > 0:
        customer.PrimaryPhone = PhoneNumber()
        customer.PrimaryPhone.FreeFormNumber = school.phoneNumbers[0]
    if len(school.phoneNumbers) > 1:
        customer.AlternatePhone = PhoneNumber()
        customer.AlternatePhone.FreeFormNumber = school.phoneNumbers[1]
    customer.BillAddr = getQuickBooksAddressFromAddress(school.address)


def getSchoolFromCustomer(customer: Customer) -> School:
    if customer is None:
        return None
    if not isinstance(customer, Customer):
        raise TypeError(f"Expected a Customer object, was {type(customer)}")

    school = School()
    school.schoolName = customer.DisplayName
    school.email = customer.PrimaryEmailAddr
    school.phoneNumbers = [customer.PrimaryPhone, customer.AlternatePhone]
    school.address = getAddressFromQuickBooksAddress(customer.BillAddr)


def getQuickBooksAddressFromAddress(address: Address) -> quickbooks.objects.Address:
    if not isinstance(address, Address):
        raise TypeError(f"Expected an Address object, was {type(address)}")

    qbAddress = quickbooks.objects.Address()
    qbAddress.Line1 = address.line1
    qbAddress.Line2 = address.line2
    qbAddress.City = address.city
    qbAddress.CountrySubDivisionCode = address.state
    qbAddress.Country = address.country
    qbAddress.PostalCode = address.zipCode

    return qbAddress


def getAddressFromQuickBooksAddress(address: quickbooks.objects.Address) -> Address:
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
