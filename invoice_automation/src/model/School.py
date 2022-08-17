from typing import List

from invoice_automation.src.model.Address import Address


class School:
    """
    Model for Schools which register for BMUN
    Corresponds 1:1 to a QuickBooks Customer
    """
    def __init__(self, schoolName: str, email: str, phoneNumbers: List[str], address: Address) -> None:
        self.schoolName = schoolName
        self.email = email
        self.phoneNumbers = phoneNumbers
        self.address = address
