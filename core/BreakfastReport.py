# import pprint
from typing import Any, Dict

import pandas as pd

from core.reports import DeliveryVehicleArrivalByHub, test_report, test_report_2
from helper.excel.save import save_large_dfs_to_excel
from helper.exceptionHandler import handle_exception
from settings import PATH_RPT_CFG, PATH_RPT_EXCEL_OUTPUT
from utils.logger import get_logger
from utils.utils import load_config

logger = get_logger(__name__)
config = load_config(PATH_RPT_CFG)


def run_breakfast_report():
    dfs = extract_data(config)
    generate_report(dfs)
    push_report_data(dfs)


def extract_data(config: Dict[str, Any]) -> dict[str, pd.DataFrame] | int:
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
        # return 2

    try:
        # raise ValueError("This is a test error to check logging")
        dfs["test_report2"] = test_report_2.extract_report_data(
            config["reports"]["test_report2"]
        )
    except Exception as e:
        handle_exception(e)
        # return 3

    try:
        dfs["DeliveryVehicleArrivalByHub"] = (
            DeliveryVehicleArrivalByHub.extract_report_data(
                config["reports"]["test_report2"]
            )
        )
    except Exception as e:
        handle_exception(e)
        # return 4

    return dfs


def generate_report(dfs):
    """
    Generates the excel file to be mailed to the stakeholders.
    """
    if isinstance(dfs, int):
        return dfs
    else:
        # list(map(logger.info, dfs.values()))
        for key, value in dfs.items():
            logger.info(f"{key}\n{value}\n")
            # pprint.pprint(value)
        save_large_dfs_to_excel(dfs, PATH_RPT_EXCEL_OUTPUT)


def push_report_data(dfs):
    """
    Pushes the generated report data to the specified destination.
    """
    try:
        # logger.warning(f"{dfs=}")
        # logger.warning(f"{dfs["test_report1"]=}")
        test_report.push_report_data(
            dfs["test_report1"], config["reports"]["test_report1"]
        )
    except Exception as e:
        logger.error(
            "The report probably failed to run \n\
                    Please ensure the dictionary has required values"
        )
        handle_exception(e)
        return 2
    pass
