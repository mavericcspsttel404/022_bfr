from typing import Any, Dict

import pandas as pd

import settings
from helper.db.extract import with_query
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_report_data(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extracts data for the specified report type from the configuration.
    """
    df = with_query(
        conn_str=getattr(settings, config["connection_string"]),
        sql=config["sql"],
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
