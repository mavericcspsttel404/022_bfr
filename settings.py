import os
import sys

from dotenv import load_dotenv

# Load environment variables
if "prod" in [arg.lower() for arg in sys.argv]:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.prod"))
else:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.uat"))
load_dotenv()

### Imports to make sure dotenv library works as expected
TEST_IMPORTS = os.getenv("TEST_IMPORTS")
TEST_IMPORTS_TEXT = os.getenv("TEST_IMPORTS_TEXT")
TEST_IMPORTS_INT = os.getenv("TEST_IMPORTS_INT")

## Imported parameters
ALFRESCO_CREDENTIALS = os.getenv("ALFRESCO_USERNAME"), os.getenv("ALFRESCO_PASSWORD")
SPIKE_ALERT_WEBHOOK = os.getenv("SPIKE_ALERT_WEBHOOK")

SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
SALESFORCE_LOGIN_URL = "https://login.salesforce.com/services/oauth2/token"

### DB Connection Strings
DB_COL06 = os.getenv("DB_COL06")
DB_COL07 = os.getenv("DB_COL07")
DB_COL10 = os.getenv("DB_COL10")
DB_DW_REPORTING = os.getenv("DB_DW_REPORTING")

BASE_URL = os.getenv("BASE_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
GRAYLOG_SERVER = os.getenv("GRAYLOG_SERVER")
GRAYLOG_PORT = os.getenv("GRAYLOG_PORT")

## Hardcoded parameters
### Logging Config
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PATH_RPT_CFG = os.path.join(BASE_PATH, "config", "reports_config.json")

if "prod" in [arg.lower() for arg in sys.argv]:
    LOG_APP_NAME = "BreakfastReport"
    SPIKE_ALERT_TITLE = "Breakfast Report Incident"
    PATH_TO_REPORTS = os.path.join(BASE_PATH, "output")
    PATH_TO_LOGS = os.path.join(BASE_PATH, "logs")
else:
    LOG_APP_NAME = "BreakfastReport - UAT"
    SPIKE_ALERT_TITLE = "Breakfast Report Incident (UAT)"
    PATH_TO_REPORTS = os.path.join(BASE_PATH, "output/uat")
    PATH_TO_LOGS = os.path.join(BASE_PATH, "logs/uat")

PATH_DVA_BY_HUB_REPORT = (
    r"//10.0.20.55/Reports/Breakfast/Delivery Vehicle Arrival By Hub.xlsx"
)
