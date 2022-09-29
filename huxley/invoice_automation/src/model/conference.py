from enum import Enum

from huxley.settings import SESSION


class Conference(Enum):
    """
    Enum representing different conferences
    Used in Registration, and to determine which line items to use when creating invoices
    """
    BMUN = f"BMUN {SESSION}"
    FC = "Fall Conference"
    TEST = "Test"
