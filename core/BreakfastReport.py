# import pprint
from typing import Any, Dict

import pandas as pd

from core.reports import test_report, test_report_2
from helper.exceptionHandler import handle_exception
from settings import PATH_RPT_CFG, PATH_RPT_EXCEL_OUTPUT
from utils.logger import get_logger
from utils.utils import load_config

logger = get_logger(__name__)
config = load_config(PATH_RPT_CFG)


def run_breakfast_report():
    dfs = extract_data(config)

    if isinstance(dfs, int):
        return dfs
    else:
        # list(map(logger.info, dfs.values()))
        for key, value in dfs.items():
            logger.info(f"{key}\n{value}\n")
            # logger.info(value)
        save_large_dfs_to_excel(dfs, PATH_RPT_EXCEL_OUTPUT)

        # for i in range(len(dfs)):
        #     logger.info(f"DataFrame {i} shape: {dfs[i].shape}")
        #     logger.info(f"DataFrame {i} columns: {dfs[i].columns.tolist()}")
        #     logger.info(f"DataFrame {i} head:\n{dfs[i].head(10)}")
        # pprint.pprint(dfs[1].head(10))


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
        return 2

    try:
        # raise ValueError("This is a test error to check logging")
        dfs["test_report2"] = test_report_2.extract_report_data(
            config["reports"]["test_report2"]
        )
    except Exception as e:
        handle_exception(e)
        return 3

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
#     save_large_dfs_to_excel()
#     pass


def save_large_dfs_to_excel(
    dfs: dict[str, pd.DataFrame],
    file_path: str,
) -> None:
    """
    Save large DataFrames to separate sheets efficiently using xlsxwriter.

    Args:
        dfs (dict): Dictionary where keys are sheet names and values are DataFrames.
        file_path (str): Path to the output Excel file (e.g., 'output.xlsx').

    Returns:
        None
    """
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        for sheet_name, df in dfs.items():
            safe_sheet_name = str(sheet_name)[:31]  # Excel sheet name limit
            df.to_excel(writer, sheet_name=safe_sheet_name, index=False)

    pass


# def push_report_data():
#     """
#     Pushes the generated report data to the specified destination.
#     """
#     pass
