from typing import List

from invoice_automation.src.model.Address import Address


class School:
    """
    Model for Schools which register for BMUN
    Corresponds 1:1 to a QuickBooks Customer

    Attributes
    ----------
    schoolName: str
        Name of the school
    email: str
        Email of school's point of contact
    phoneNumbers: List[str]
        School's primary phone number, optional secondary phone number
    address: Address
        School's billing address
    id: str
        Id of QB Customer corresponding to this school
    """

    def __init__(self, schoolName: str, email: str, phoneNumbers: List[str], address: Address) -> None:
        self.schoolName = schoolName
        self.email = email
        self.phoneNumbers = phoneNumbers
        self.address = address
        self.id = None
