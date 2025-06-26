import logging
import os

BASE_PATH = os.path.dirname(__file__)
PATH_TO_REPORTS = os.path.join(BASE_PATH, "spreadsheets")
PATH_TO_LOGS = os.path.join(BASE_PATH, "logs\\reports.log")
PATH_DVA_BY_HUB_REPORT = (
    r"//10.0.20.55/Reports/Breakfast/Delivery Vehicle Arrival By Hub.xlsx"
)

BASE_URL = "http://10.0.20.53:8080" 
ALFRESCO_CREDENTIALS = "admin", "Admin 1024"

SPIKE_ALERT_WEBHOOK = "https://hooks.spike.sh/53ba64/push-events"
SPIKE_ALERT_TITLE = "Breakfast Report Incident"

SALESFORCE_USERNAME = "companyapi@company.co.za"
SALESFORCE_PASSWORD = "mYveh9"
SALESFORCE_CLIENT_ID = "3MVG9tzXBVPH"
SALESFORCE_CLIENT_SECRET = (
    "C17DDE3"
)
SALESFORCE_LOGIN_URL = "https://login.salesforce.com/services/oauth2/token"


# DB Connection Strings
DB_COL06_companyTNTV1 = "DRIVER={SQL Server};SERVER=companysqlcol06;DATABASE=companyTnTv1;UID=companysqladmin;PWD=fkinchangeme;unicode_results=True"
DB_COL10_companyTNTV1 = "DRIVER={SQL Server};SERVER=companysqlcol10;DATABASE=companyTnTv1;UID=companysqladmin;PWD=fkinchangeme;unicode_results=True"
DB_COL07_UAT_companyTNTV1 = "DRIVER={SQL Server};SERVER=companysqlcol07-uat;DATABASE=companyTnTv1;UID=companysqladmin;PWD=fkinchangeme;unicode_results=True"
DB_COL07_companyTNTV1 = "DRIVER={SQL Server};SERVER=companysqlcol07;DATABASE=companyTnTv1;UID=companysqladmin;PWD=fkinchangeme;unicode_results=True"
DB_DW_UAT_REPORTING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=UATSQLINSTANCE;DATABASE=Reporting;UID=companysqladmin;PWD=fkinchangeme2019;unicode_results=True"
DB_DW_REPORTING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=PRODSQLINSTANCE;DATABASE=Reporting;UID=companysqladmin;PWD=fkinchangeme2020;unicode_results=True"

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
