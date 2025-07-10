from typing import Any, Dict

import pandas as pd

from settings import PATH_DVA_BY_HUB_REPORT
from utils.logger import get_logger

logger = get_logger


def extract_report_data(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extracts data for the specified report type from the configuration.
    """
    df = pd.read_excel(PATH_DVA_BY_HUB_REPORT)
    return df
