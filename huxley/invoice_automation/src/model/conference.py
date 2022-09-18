from enum import Enum


class Conference(Enum):
    """
    Enum representing different conferences
    Used in Registration, and to determine which line items to use when creating invoices
    """
    BMUN71 = "BMUN 71"
    FC = "Fall Conference"
    TEST = "Test"
