from typing import List

from intuitlib.client import AuthClient

from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects.customer import Customer


# TODO: Replace with prod versions during deployment
# Should probably move these to settings/main.py at some point
# Quickbooks constants
from invoice_automation.src.model.School import School
from invoice_automation.src.util import QuickBooksUtils

CLIENT_ID = "ABYdHrqfKuQBK7bDiZpCK9C6Cq9bhayJJZbPCRyJLu7rO2nNqX"
CLIENT_SECRET = "KKJQ9uQJdlydvcCZigkZ3PlbEXQ8ZUjohKrEwzjN"
COMPANY_ID = "4620816365199192370"

# Quickbooks tokens
REFRESH_TOKEN = "AB11667363349c93rhkisENljWb2z9zKRD3ltFWU3WmM8WMAoP"

class QuickBooksModule:
    """
    Abstraction barrier for calling QuickBook API's
    """
    def __init__(self) -> None:
        self.authClient = AuthClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://localhost:8000/callback",
            environment="sandbox"
        )
        try:
            self.quickBooksClient = QuickBooks(
                auth_client=self.authClient,
                refresh_token=REFRESH_TOKEN,
                company_id=COMPANY_ID
            )
            self.authClient.refresh(refresh_token=REFRESH_TOKEN)
            print(Customer.all(qb=self.quickBooksClient))
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)

    def querySchoolsAsCustomers(self, schoolNames: List[str]) -> List[School]:
        qbCustomers = Customer.choose(schoolNames, "DisplayName", self.quickBooksClient)
        return [QuickBooksUtils.getSchoolFromCustomer(customer) for customer in qbCustomers]

QuickBooksModule()
