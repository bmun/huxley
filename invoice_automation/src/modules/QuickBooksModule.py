from intuitlib.client import AuthClient

from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException
from quickbooks.objects.customer import Customer

from huxley.settings import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN

# TODO: The below need to be replaced with their prod versions before deployment
# The prod versions should never be exposed publicly


class QuickBooksModule:
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
                refresh_token=REFRESH_TOKEN
            )
            print(Customer.all(qb=self.quickBooksClient))
        except QuickbooksException as e:
            print(e.message)
            print(e.error_code)
            print(e.detail)


QuickBooksModule()
