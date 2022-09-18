import datetime

from huxley.invoice_automation.src.model.conference import Conference
from huxley.invoice_automation.src.model.payment_method import PaymentMethod
from huxley.invoice_automation.src.model.school import School


class Registration:
    """
    Represents a school's registration for a particular conference

    Attributes
    ----------
    school: School
        School object corresponding to registering school
    num_delegates: int
        Number of delegates registering
    conference: Conference
        Which conference the school is registering for
    registration_date: datetime.datetime
        Date the registration was made
        Used to determine the due date
    """

    def __init__(self,
                 school: School,
                 num_delegates: int,
                 conference: Conference,
                 registration_date: datetime.datetime,
                 payment_method: PaymentMethod) -> None:
        self.school = school
        self.num_delegates = num_delegates
        self.conference = conference
        self.registration_date = registration_date
        self.payment_method = payment_method
