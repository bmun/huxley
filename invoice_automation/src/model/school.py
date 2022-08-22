from typing import List

from invoice_automation.src.model.address import Address


class School:
    """
    Model for Schools which register for BMUN
    Corresponds 1:1 to a QuickBooks Customer

    Attributes
    ----------
    school_name: str
        Name of the school
    email: str
        Email of school's point of contact
    phone_numbers: List[str]
        School's primary phone number, optional secondary phone number
    address: Address
        School's billing address
    id: str
        ID of QB Customer corresponding to this school
    """

    def __init__(self,
                 school_name: str,
                 email: str = None,
                 phone_numbers: List[str] = None,
                 address: Address = None) -> None:
        self.school_name = school_name
        self.email = email
        self.phone_numbers = phone_numbers
        self.address = address
        self.id = None
