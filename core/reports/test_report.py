from typing import Any, Dict

import pandas as pd

import settings
from helper.db.extract import with_stored_procedure
from helper.db.push import bulk_insert_dataframe
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_report_data(
    config: Dict[str, Any], **kwargsconfig: Dict[str, Any]
) -> pd.DataFrame:
    """
    Extracts data for the specified report type from the configuration.
    """
    # logger.info("*************************************")
    # logger.info(config)
    # logger.info(settings.DB_COL06)
    # logger.info(getattr(settings, config["connection_string"]))
    # raise ValueError("This is a test error to check logging")
    df = with_stored_procedure(
        conn_str=getattr(settings, config["connection_string"]),
        proc_name=config["proc_name"],
        params=config.get("params", []),
    )
    return df


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
        # push_connection_string is used for inserting the report data
        conn_str=getattr(settings, config["push_connection_string"]),
        table_name=config["table_name"],
        df=df,
        columns=None,
        expected_schema=None,
        schema_file=config["schema_file"],
        rename_map=None,
    )
