import datetime

import pandas as pd
import requests
from simple_salesforce.api import Salesforce

from settings import (
    SALESFORCE_PASSWORD,
    SALESFORCE_SECURITY_TOKEN,
    SALESFORCE_USERNAME,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def get_cases_from_salesforce(
    start_dt: datetime.date = datetime.date.today()
    - datetime.timedelta(days=1),
    end_dt: datetime.date = datetime.date.today(),
    chunk=30000,
):
    format_string = "%Y-%m-%dT00:00:01Z"  # salesforce format requirement
    end = end_dt.strftime(format_string)
    start = start_dt.strftime(format_string)

    select = """
        SELECT Id,
            CaseNumber,
            Case_Type__c,
            CreatedDate,
            ClosedDate,
            Delivery_Attempts__c,
            Status,
            Subject,
            Consignment_Name__c,
            Consignment_ID__c,
            NDV_Task_Validated_Reason__c,
            Non_Delivery_Reason_Selected__c,
            Non_Delivery_Reason__c,
            NDV_Task_Outcome__c,
            QM_CCC_Outcome__c,
            QM_RTS_Outcome__c,
            COA_Task_Outcome__c,
            IHA_Outcome__c,
            SM_Result__c,
            Contact.Name
        FROM Case
        """
    where = f""" WHERE CreatedDate > {start}
    AND CreatedDate < {end}
    AND Case_Type__c IN ('Non-Delivery Validation','Missed Delivery')
    """

    session = requests.Session()
    sf = Salesforce(
        username=SALESFORCE_USERNAME,
        password=SALESFORCE_PASSWORD,
        security_token=SALESFORCE_SECURITY_TOKEN,
        client_id="Breakfast Report",
        session=session,
    )
    query = str(select) + str(where)
    logger.debug(query)
    response = sf.bulk.Case.query(query)  # type: ignore
    return pd.DataFrame(response)
