from datetime import datetime
from typing import Any, Dict

import pandas as pd

import settings
from helper.db.extract import with_stored_procedure
from helper.db.push import bulk_insert_dataframe
from helper.salesforce.extract import get_cases_from_salesforce
from utils import utils
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_report_data(config: Dict[str, Any]) -> None:  # pd.DataFrame:
    """
    Extracts data for the specified report type from the configuration.
    """
    # ^ result 2 - deliveryExceptions from db
    df = with_stored_procedure(
        conn_str=getattr(settings, config["connection_string"]),
        proc_name=config["proc_name"],
        params=config.get("params", []),
    )

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    columns = settings.COLUMNS_DELIVERY_EXCEPTIONS_SALESFORCE
    logger.debug(f"Getting Salesforce case data {datetime.now()}")

    data = get_cases_from_salesforce(start_dt="", end_dt="")
    if data.empty:
        logger.info("Empty Salesforce case data, skipping processing")
        return

    logger.debug(f"Got Salesforce case data {datetime.now()}")
    data = transform_salesforce_data(data)
    result2 = merge_and_enrich_data(data, df)
    result2 = format_and_calculate_fields(result2)

    logger.debug(f"Formatting done {datetime.now()}")
    # result2 = utils.filter_and_order_df(result2)
    logger.debug(f"Filter and order done {datetime.now()}")


def transform_salesforce_data(data):
    data["SM_Result__c"] = data["SM_Result__c"].apply(utils.flatten_json)
    res = [val for val in data["SM_Result__c"].tolist() if val != {}]

    if res:
        result_DF = pd.DataFrame(res)
        result_DF.rename(
            columns={
                "ConsignmentId": "ConsignmentRecordID",
                "consignmentName": "ConsignmentID",
            },
            inplace=True,
        )
        data = data.merge(result_DF, how="left", on="ConsignmentID")
    else:
        logger.info("No nested SM_Result__c data found, using fallback columns")

    return data


def merge_and_enrich_data(data, result2):
    # ! make sure to merge sfdata on db data like below
    # ! data = data.merge(result_DF, how='left', on='ConsignmentID')
    result2 = result2.merge(data, how="left", on="ConsignmentID")
    logger.debug(f"Completed merge {datetime.now()}")

    result2["CreatedDate"] = pd.to_datetime(
        result2["CreatedDate"], format="%Y-%m-%d %H:%M:%S"
    )
    result2["ClosedDate"] = pd.to_datetime(
        result2["ClosedDate"], format="%Y-%m-%d %H:%M:%S"
    )
    logger.debug(f"Sorted out dates {datetime.now()}")

    result2["Time Taken To Resolve Task"] = result2.apply(
        utils.calc_time_ND_from_case_data, axis=1
    )
    logger.debug(f"Calculated time taken to resolve case {datetime.now()}")

    return result2


def format_and_calculate_fields(result2):
    logger.debug(f"Starting formatting of the data {datetime.now()}")

    result2["NonDeliveryDT"] = pd.to_datetime(
        result2["NonDeliveryDT"], format="%Y-%m-%d %H:%M:%S"
    )
    result2["NonDeliveryDate"] = result2["NonDeliveryDT"].dt.date
    result2["Time ND on Mobile"] = result2["NonDeliveryDT"].apply(
        utils.time_from_datetime
    )
    result2["NDV_Task_Outcome__c"] = result2.apply(
        utils.fix_case_outcome, axis=1
    )
    result2["Time Bracket"] = result2["NonDeliveryDT"].apply(
        utils.get_timeBracket_from_time
    )

    for col in [
        "CrewEmployeeNo",
        "CrewName",
        "CustomerGroupID",
        "FullAddress",
        "Suburb",
        "Area",
        "Township",
    ]:
        result2[col] = result2[col].apply(utils.replace_system_account)

    return result2


def generate_report():
    """
    Generates the excel file to be mailed to the stakeholders.
    """
    pass


def push_report_data(df, config: Dict[str, Any]):
    """
    Pushes the generated report data to the specified destination.
    """
    bulk_insert_dataframe(
        # conn_str=getattr(settings, config["connection_string"]),
        conn_str=getattr(settings, config["push_connection_string"]),
        table_name=config["table_name"],
        df=df,
        columns=None,
        expected_schema=None,
        schema_file=config["schema_file"],
        rename_map=None,
    )
