import logging
import os

# Load secrets from environment variables

BASE_PATH = os.path.dirname(__file__)
PATH_TO_REPORTS = os.path.join(BASE_PATH, "spreadsheets")
PATH_TO_LOGS = os.path.join(BASE_PATH, "logs\\reports.log")
PATH_DVA_BY_HUB_REPORT = (
    r"//10.0.20.55/Reports/Breakfast/Delivery Vehicle Arrival By Hub.xlsx"
)

BASE_URL = "http://10.0.20.53:8080" 
ALFRESCO_CREDENTIALS = os.getenv("ALFRESCO_USERNAME"), os.getenv("ALFRESCO_PASSWORD")

SPIKE_ALERT_WEBHOOK = os.getenv("SPIKE_ALERT_WEBHOOK")
SPIKE_ALERT_TITLE = "Breakfast Report Incident"

SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
SALESFORCE_LOGIN_URL = "https://login.salesforce.com/services/oauth2/token"


# DB Connection Strings
DB_COL06_companyTNTV1 = os.getenv("DB_COL06_companyTNTV1")
DB_COL10_companyTNTV1 = os.getenv("DB_COL10_companyTNTV1")
DB_COL07_UAT_companyTNTV1 = os.getenv("DB_COL07_UAT_companyTNTV1")
DB_COL07_companyTNTV1 = os.getenv("DB_COL07_companyTNTV1")
DB_DW_UAT_REPORTING = os.getenv("DB_DW_UAT_REPORTING")
DB_DW_REPORTING = os.getenv("DB_DW_REPORTING")

# Logging Config
LOG_LEVEL = logging.DEBUG
GRAYLOG_SERVER = "10.0.20.82"
LOG_APP_NAME = "BreakfastReport"


# Report Columns and ordering
COLUMNS_ND = [
    "processId",
    "id",
    "processDefinitionKey",
    "properties:followingProcessDefinitionKey",
    "properties:followingProcessId",
]

COLUMNS_COA = [
    "processId",
    "id",
    "processDefinitionKey",
    "properties:oldAddressCountry",
    "properties:oldAddressHubID",
]

COLUMNS_CCC = [
    "processId",
    "id",
    "processDefinitionKey",
    "properties:initiatingProcessId",
    "name",
    "isOpen",
    "properties:newLat",
]

COLUMNS_CANCELLED = [
    "processId",
    "id",
    "processDefinitionKey",
    "properties:initiatingProcessId",
    "name",
    "isOpen",
    "properties:newLong",
    "properties:newLat",
]

COLUMNS_DELIVERY_EXCEPTIONS = [
    "ConsignmentID",
    "NonDeliveryDate",
    "startedAt",
    "completedAt",
    "Time Taken To Resolve Task",
]

COLUMNS_DELIVERY_EXCEPTIONS_SALESFORCE = [
    "ConsignmentID",
    "NonDeliveryDate",
    "FullAddress",
    "Suburb",
    "Area",
    "Township",
]

COLUMNS_DELIVERY_EXCEPTIONS_SALESFORCE_EMPTY = [
    "ConsignmentID",
    "NonDeliveryDate",
    "CustomerGroupID",
    "FullAddress",
    "Suburb",
    "Area",
    "Township",
]


# Report Record Filters
FILTER_ND = []

FILTER_COA = ["Resolve Query", "Query Escalation"]

FILTER_CCC = ["Resolve Query", "Query Escalation"]

FILTER_CANCELLED = ["Resolve Query", "Query Escalation"]

FILTER_BREAKFAST = ["Confirm ND Reason"]
