from typing import Any, Dict

import pandas as pd

import settings
from core.db.extract import with_stored_procedure
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_report_data(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extracts data for the specified report type from the configuration.
    """
    # logger.info("*************************************")
    # logger.info(config)
    # logger.info(settings.DB_COL06)
    # logger.info(getattr(settings, config["connection_string"]))
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


def push_report_data():
    """
    Pushes the generated report data to the specified destination.
    """
    pass
