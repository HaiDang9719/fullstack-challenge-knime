from flask import jsonify
from pandas.io.json import json_normalize
import numpy as np
import pandas as pd
import math
import ast
import json
import time
def df_to_dict(df):
    """
    Converts a pandas data frame to dictionary.
    :param df: A pandas data frame
    :return: The df converted as dictionary
    """
    return df.to_dict(orient='records')

def df_to_json(df):
    """
    Converts a pandas data frame to json.
    :param df: A pandas data frame
    :return: The df converted to a JSON list
    """
    return jsonify(df_to_dict(df))

def array_to_df(array):
    return pd.DataFrame(array)