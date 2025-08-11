import decimal
import json
from datetime import datetime
from typing import Dict, Type

from utils.logger import get_logger

logger = get_logger(__name__)

PYTHON_TYPE_MAP: dict[str, Type] = {
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "decimal": decimal.Decimal,
}


def load_config(config_file: str) -> dict:
    """Load the configuration from the JSON file."""
    with open(config_file, "r") as f:
        return json.load(f)


def read_sql_query(query_file: str) -> str:
    """Reads an SQL query from a .sql file."""
    with open(query_file, "r") as file:
        return file.read()


def load_schema(schema_file: str) -> Dict[str, Type]:
    """Load a JSON schema file and convert type strings to Python types."""
    raw_schema = load_config(schema_file)
    return {
        col: PYTHON_TYPE_MAP[type_str] for col, type_str in raw_schema.items()
    }


# def filter_and_order_df(df):
#     try:
#         # reorder the columns
#         if columns != None:
#             logger.debug(
#                 "Starting reorder of DF "
#                 + report_name
#                 + " "
#                 + str(datetime.now())
#             )
#             df = df[columns]

#         # sort the DataFrame
#         # print("Starting sort of DF " + report_name + " " + str(datetime.now()))
#         # df = df.sort_values('processId')

#         # filter the DF if there is a filter specified
#         if not filter == None:
#             logger.debug(
#                 "Starting filter of DF "
#                 + report_name
#                 + " "
#                 + str(datetime.now())
#             )
#             df = df[df.name.isin(filter)]
#         return df
#     except Exception as e:
#         logger.exception(e)
#         return pd.DataFrame()


def calc_time_ND_from_case_data(x):
    try:
        if x["CreatedDate"] != x["CreatedDate"]:
            logger.debug(
                "x['CreatedDate'] not a datetime",
                extra={
                    "input": {
                        "Consignment_Name__c": x["Consignment_Name__c"],
                        "CreatedDate": x["CreatedDate"],
                        "ClosedDate": x["ClosedDate"],
                    }
                },
            )
            return ""
        else:
            sdt = x["CreatedDate"]
            edt = x["ClosedDate"]
            # if isinstance(edt, datetime):
            #    start = datetime.strptime(str(sdt) , '%Y/%m/%d %H:%M:%S')
            #    end = datetime.strptime(str(edt) , '%Y/%m/%d %H:%M:%S')
            #    elapsedTime  = end - start

            # start = datetime.strptime(str(sdt), '%Y-%m-%dT%H:%M:%S.000+0000') # '2020-10-06T22:15:13.000+0000'
            # end = datetime.strptime(str(edt), '%Y-%m-%dT%H:%M:%S.000+0000')
            start = datetime.strptime(str(sdt), "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(str(edt), "%Y-%m-%d %H:%M:%S")
            elapsedTime = end - start
            minutesTotal = elapsedTime.total_seconds() / 60
            hours, minutes = divmod(minutesTotal, 60)
            minutes = int(minutes)
            hours = int(hours)
            min = str(int(minutes))
            if len(min) == 1:
                min = "0" + min

            return str(hours) + ":" + min
            # return str(int(minutesTotal))

        logger.debug(
            "x['CreatedDate'] not a datetime",
            extra={
                "input": {
                    "Consignment_Name__c": x["Consignment_Name__c"],
                    "CreatedDate": x["CreatedDate"],
                    "ClosedDate": x["ClosedDate"],
                }
            },
        )
        return ""
    except KeyError:
        return ""
    except Exception:
        # logger.error("Error calculating time from ND", stack_info=True, extra={"input": x})
        # logger.exception(e)
        # print('Failed to calc time difference: ' + str(e))
        return ""


def flatten_json(y):
    out = {}
    try:
        if len(str(y)) > 15:
            dictionary = json.loads(str(y))

            def flatten(x, name=""):
                if type(x) is dict:
                    for a in x:
                        flatten(x[a], name + a + "_")
                elif type(x) is list:
                    i = 0
                    for a in x:
                        flatten(a, name + str(i) + "_")
                        i += 1
                else:
                    out[name[:-1]] = x

            flatten(dictionary)
        else:
            return out

    except Exception as e:
        logger.exception(e)
        logger.debug(y)
    # out = fd.FlatDict(y)

    return out
    # return json.dumps(out)


def time_from_datetime(d):
    try:
        if d != d:
            # logger.debug("d not a datetime", extra={"input": {"d": str(d)}})
            return "00:00:00"
        else:
            time = str(d.time())
            time = time.split(".")[0]
            return time

    except Exception as e:
        logger.error(
            "Error getting time from datetime",
            stack_info=True,
            extra={"input": d},
        )
        logger.exception(e)
        return "00:00:00"


def fix_case_outcome(x):
    string = None
    try:
        string = x["NDV_Task_Outcome__c"]
        caseType = x["Case_Type__c"]

        if isinstance(caseType, str):
            if len(caseType) < 2:
                return "No Case Created"
        else:
            return "No Case Created"
        # logger.debug("string is not a string", extra={"input": {"string": str(string)}})
        if isinstance(string, str):
            if len(string) < 2:
                return "Case Not Actioned"
            return string
        else:
            return "Case Not Actioned"

    except Exception as e:
        logger.error(
            "Error fixing outcome from ND",
            stack_info=True,
            extra={"input": string},
        )
        logger.exception(e)
        return "UNKNOWN"


def get_timeBracket_from_time(string):
    try:
        if string != string:
            # logger.debug("string is not a datetime", extra={"input": {"string": str(string)}})
            return "No Mobile Time"
        else:
            string = "{0:%H}".format(string)

            hour = int(string)
            eh = str(hour + 1)

            # pad digits
            if len(eh) == 1:
                eh = "0" + eh
            sh = str(hour)
            if len(sh) == 1:
                sh = "0" + sh

            return "'{s} - {e}".format(s=sh, e=eh)

    except Exception as e:
        logger.exception(e)
        return "UNKNOWN"


def get_dataframe_from_salesforce():
    # raise Exception("Not Implemented Yet")
    pass


def replace_system_account(string):
    if string == "0000" or string == "SYSTEM ACCOUNT":
        return ""
    return string
