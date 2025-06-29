from settings import PATH_RPT_CFG
from utils.utils import load_config

config = load_config(PATH_RPT_CFG)
# print(config)


def extract_report_data():
    """
    Extracts data for the specified report type from the configuration.
    """
    pass


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
