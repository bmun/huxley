from invoice_automation.src.model.registration import Registration
from invoice_automation.src.module.quick_books_module import QuickBooksModule


class RegistrationHandler:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 refresh_token="",
                 realm_id="",
                 access_token=""):
        self.quickbooks_module = QuickBooksModule(client_id, client_secret, refresh_token, realm_id, access_token)

    def handle_registration(self, registration: Registration):
        customer = self.quickbooks_module.update_or_create_customer_from_school(registration.school)

        invoice = self.quickbooks_module.query_invoice_from_registration(registration)

        if invoice is None:
            invoice = self.quickbooks_module.create_invoice_from_registration(
                registration,
                customer.PrimaryEmailAddr.Address
            )

        if not invoice.email_sent:
            self.quickbooks_module.send_invoice(invoice)
