# import pprint
from typing import Any, Dict

import pandas as pd

from core.exceptionHandler import handle_exception
from core.reports import test_report, test_report_2
from settings import PATH_RPT_CFG
from utils.logger import get_logger
from utils.utils import load_config

logger = get_logger(__name__)
config = load_config(PATH_RPT_CFG)
# print(config)

logger.info("here")


def generate_breakfast_report():
    dfs = extract_data(config)

    # list(map(logger.info, dfs.values()))
    for value in dfs.values():
        logger.info(f"\n{value}")
        # logger.info(value)

    # for i in range(len(dfs)):
    #     logger.info(f"DataFrame {i} shape: {dfs[i].shape}")
    #     logger.info(f"DataFrame {i} columns: {dfs[i].columns.tolist()}")
    #     logger.info(f"DataFrame {i} head:\n{dfs[i].head(10)}")
    # pprint.pprint(dfs[1].head(10))
    pass


def extract_data(config: Dict[str, Any]) -> dict[str, pd.DataFrame]:
    """
    Extracts data for the breakfast report.
    """
    dfs = {}
    # logger.info(config["reports"]["test_report1"])
    try:
        dfs["test_report1"] = test_report.extract_report_data(
            config["reports"]["test_report1"]
        )
    except Exception as e:
        handle_exception(e)

    # raise ValueError("This is a test error to check logging")
    dfs["test_report2"] = test_report_2.extract_report_data(
        config["reports"]["test_report2"]
    )
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
