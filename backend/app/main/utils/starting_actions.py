import sys
import os
import pandas as pd
from operator import itemgetter
from app.main.utils.config_reader import application as app_config
from app.main.utils.config_reader import indices as es_indices_config

from app.main.utils.es_connection import ESConnection

def create_data_index():
    es = ESConnection(index=es_indices_config['data_index'])
    es.create_index(delete_if_exists=app_config['clear_data_index_at_startup'])
    # es.create_index(delete_if_exists=True)