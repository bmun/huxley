import datetime

from pypika import Query
from pypika.terms import PseudoColumn
from quickbooks.objects import Ref

INVOICE_FILTER_START_DATE = datetime.datetime(2022, 8, 1)


def construct_invoice_query(customer_ref: Ref) -> str:
    """
    Constructs invoice query
    Matches customer_ref and looks for all invoices from 8/1/22 onward
    :param customer_ref:
    :return:
    """
    customer_ref_value_column = PseudoColumn("CustomerRef")
    create_time_column = PseudoColumn("MetaData.CreateTime")

    return str(
        Query.from_("Invoice")
        .select("*")
        .where(customer_ref_value_column == customer_ref.value)
        .where(create_time_column >= INVOICE_FILTER_START_DATE)
    ).replace("\"Invoice\"", "Invoice")
