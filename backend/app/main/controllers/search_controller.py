from app.main.controllers.controller import Controller
from datetime import datetime

import json

class SearchController(Controller):
    def __init__(self):
        super().__init__()
        self._add_args()
        self.userKey = ''
        self.es_index = 'node-information'

    def _add_args(self):
        super()._add_args()

    def process_args(self):
        super().process_args()
    
    def get_node_information_data(self):
        cache_record = self.es.get_all_records_from_index(self.es_index)
        if len(cache_record) > 0:
            return cache_record
        else:
            default_node_info = [{'name': 'Column Expressions', 'tag': 'KNIME Labs, Streamable', 'group': 'Node/Manipulator', 'description': 'This node provides the possibility to append an arbitrary number ...'},\
                {'name': 'File Reader', 'tag': 'IO, Read, Streamable', 'group': 'Node/Source', 'description': 'Reads the most common text files.  ...'}]
            for no in default_node_info:
                self.add_node_information_data(no)
            cache_record = self.es.get_all_records_from_index(self.es_index)
            return cache_record
    
    
    
    def add_node_information_data(self, node_info_data):
        try:
            return self.es.store_record_withoutID({'value': node_info_data}, self.es_index)
        except Exception as e:
            print('Error in add_node_information_data: ', str(e), flush=True)
    
    def update_node_information_data(self, node_info_data, record_id):
        try:
            return self.es.store_record_to_index({'value': node_info_data}, record_id ,self.es_index)
        except Exception as e:
            print('Error in update_node_information_data: ', str(e), flush=True)

    def delete_node_information_data(self, record_id):
        try:
            return self.es.delete_record_from_index_by_id(record_id ,self.es_index)
        except Exception as e:
            print('Error in delete_node_information_data: ', str(e), flush=True)

    
    def search_node_by_value(self, search_value):
        cache_record_name = self.es.get_record_from_index_by_search_string_in_name(search_value, self.es_index)
        cache_record_tag = self.es.get_record_from_index_by_search_string_in_tag(search_value, self.es_index)
        id_list = []
        result = []
        for cache_name in cache_record_name:
            if cache_name['record_id'] not in id_list:
                id_list.append(cache_name['record_id'])
                result.append(cache_name)
        for cache_tag in cache_record_tag:
            if cache_tag['record_id'] not in id_list:
                id_list.append(cache_tag['record_id'])
                result.append(cache_tag)
        return result