import pprint
from typing import Any, Dict, List

import pandas as pd

from core.reports import test_report
from settings import PATH_RPT_CFG
from utils.logger import get_logger
from utils.utils import load_config

logger = get_logger(__name__)
config = load_config(PATH_RPT_CFG)
# print(config)

logger.info("here")


def generate_breakfast_report():
    dfs = extract_data(config)
    pprint.pprint(dfs[0].head(10))
    pass


def extract_data(config: Dict[str, Any]) -> List[pd.DataFrame]:
    """
    Extracts data for the breakfast report.
    """
    dfs = []
    # logger.info(config["reports"]["test_report1"])
    dfs.append(test_report.extract_report_data(config["reports"]["test_report1"]))
    return dfs


# def extract_report_data():
#     """
#     Extracts data for the specified report type from the configuration.
#     """
#     pass


# def generate_report():
#     """
#     Generates the excel file to be mailed to the stakeholders.
#     """
#     pass


# def push_report_data():
#     """
#     Pushes the generated report data to the specified destination.
#     """
#     pass
