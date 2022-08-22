"""
This module contains the constants which comprise the paths used
in calls to patch in unit tests

Some paths may need to renamed in future to prevent collisions
An alternative could be to use dictionaries for each module mapping
each target object to its path from the perspective of that module
"""

INVOICE_AUTOMATION = "invoice_automation"
SRC = "src"

# Util names
UTIL = "util"
QUICK_BOOKS_UTILS = "quick_books_utils"
GET_QUICKBOOKS_ADDRESS_FROM_ADDRESS = "get_quickbooks_address_from_address"
GET_ADDRESS_FROM_QUICKBOOKS_ADDRESS = "get_address_from_quickbooks_address"
GET_SCHOOL_FROM_CUSTOMER = "get_school_from_customer"
GET_CUSTOMER_FROM_SCHOOL = "get_customer_from_school"
CONFERENCE_TO_LINE_ITEM_NAMES = "CONFERENCE_TO_LINE_ITEM_NAMES"
CHECK_INVOICE_MATCHES_ITEMS_AND_COUNTS = "check_invoice_matches_items_and_counts"

CONSTRUCT_INVOICE_QUERY = "construct_invoice_query"

# Module names
MODULE = "module"
QUICK_BOOKS_MODULE = "quick_books_module"
GET_CUSTOMER_REF_FROM_SCHOOL = "get_customer_ref_from_school"
QUERY_INVOICES_FROM_CUSTOMER_REF = "query_invoices_from_customer_ref"

# intuit-lib names
AUTHCLIENT = "AuthClient"

# quickbooks names
QUICKBOOKS_CLIENT = "QuickBooks"
CUSTOMER = "Customer"
ITEM = "Item"
INVOICE = "Invoice"
CHOOSE = "choose"
QUERY = "query"

# actual paths start here:
SRC_PATH = INVOICE_AUTOMATION + "." + SRC

# test_quick_books_utils
QUICK_BOOKS_UTILS_PATH = ".".join([SRC_PATH, UTIL, QUICK_BOOKS_UTILS])
GET_QUICKBOOKS_ADDRESS_FROM_ADDRESS_PATH = QUICK_BOOKS_UTILS_PATH + "." + GET_QUICKBOOKS_ADDRESS_FROM_ADDRESS
GET_ADDRESS_FROM_QUICKBOOKS_ADDRESS_PATH = QUICK_BOOKS_UTILS_PATH + "." + GET_ADDRESS_FROM_QUICKBOOKS_ADDRESS


# test_quick_books_module
QUICK_BOOKS_MODULE_PATH = ".".join([SRC_PATH, MODULE, QUICK_BOOKS_MODULE])
AUTHCLIENT_PATH = QUICK_BOOKS_MODULE_PATH + "." + AUTHCLIENT
QUICKBOOKS_CLIENT_PATH = QUICK_BOOKS_MODULE_PATH + "." + QUICKBOOKS_CLIENT
CUSTOMER_CHOOSE_PATH = ".".join([QUICK_BOOKS_MODULE_PATH, CUSTOMER, CHOOSE])
ITEM_CHOOSE_PATH = ".".join([QUICK_BOOKS_MODULE_PATH, ITEM, CHOOSE])
INVOICE_QUERY_PATH = ".".join([QUICK_BOOKS_MODULE_PATH, INVOICE, QUERY])
GET_SCHOOL_FROM_CUSTOMER_PATH = ".".join([QUICK_BOOKS_MODULE_PATH, QUICK_BOOKS_UTILS, GET_SCHOOL_FROM_CUSTOMER])
GET_CUSTOMER_FROM_SCHOOL_PATH = ".".join([QUICK_BOOKS_MODULE_PATH, QUICK_BOOKS_UTILS, GET_CUSTOMER_FROM_SCHOOL])
CONFERENCE_TO_LINE_ITEM_NAMES_PATH = "."\
    .join([QUICK_BOOKS_MODULE_PATH, QUICK_BOOKS_UTILS, CONFERENCE_TO_LINE_ITEM_NAMES])
CONSTRUCT_INVOICE_QUERY_PATH = QUICK_BOOKS_MODULE_PATH + "." + CONSTRUCT_INVOICE_QUERY
CHECK_INVOICE_MATCHES_ITEMS_AND_COUNTS_PATH = QUICK_BOOKS_MODULE_PATH + "." + CHECK_INVOICE_MATCHES_ITEMS_AND_COUNTS
