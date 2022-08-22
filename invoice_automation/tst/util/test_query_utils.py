from quickbooks.objects import Ref

from invoice_automation.src.util.query_utils import construct_invoice_query


class TestQueryUtils:
    def test_construct_invoice_query_happyPath(self):
        # Setup
        customer_ref = Ref()
        customer_ref.value = 1

        # Act
        query = construct_invoice_query(customer_ref)

        # Verify
        expected_query = 'SELECT * FROM Invoice WHERE CustomerRef=1 AND MetaData.CreateTime>=\'2022-08-01T00:00:00\''
        assert query == expected_query
