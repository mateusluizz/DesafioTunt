import gspread
import pandas as pd
import numpy as np
from constants import CREDENTIALS


def get_sheet_data(url_key: str, sheet_name: str) -> pd.DataFrame:
    """
    Opens a Google's spreadsheet

    :param url_key: A key of a spreadsheet as it appears in a URL in a browser
    :param sheet_name: A title of a worksheet. If there are multiple worksheets with the same title, first one will be returned.
    :return: A pandas Dataframe containing all data
    """
    gc = gspread.service_account(filename=CREDENTIALS)
    data = (
        gc
        .open_by_key(url_key)
        .worksheet(sheet_name)
        .get_all_values()
    )
    return data
