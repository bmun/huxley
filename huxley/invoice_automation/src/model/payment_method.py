from enum import Enum, auto


class PaymentMethod(Enum):
    Check = auto()
    Card = auto()