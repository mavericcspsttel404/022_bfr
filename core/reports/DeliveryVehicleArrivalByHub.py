import os
from typing import Any, Dict

import pandas as pd

from helper.excel.extract import handle_excel_file

# from settings import PATH_DVA_BY_HUB_REPORT
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_report_data(config: Dict[str, Any]) -> pd.DataFrame:
    # df = handle_excel_file(PATH_DVA_BY_HUB_REPORT)
    df = handle_excel_file(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "output", "result.xlsx"
        )
    )
    # transformation steps if any
    return df
