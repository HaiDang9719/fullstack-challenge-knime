from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search

# from ..model.dataset import Entity, Feature, EntityNew
# from ..utils.query_util import compute_timestamp_ranges, aggregation_function_for_value_type, field_for_value_type, field_for_value_type_for_feature
from ..utils.config_reader import elastic as es_config
from ..utils.config_reader import indices as es_indices_config
from ..utils.es_config_reader import elastic_index_config as elastic_index_config
from ..utils.data_transformation import df_to_dict
import pandas as pd
import sys
import datetime
import json
class ESConnection(object):

    def __init__(self,
                 index=es_indices_config['data_index'],
                 host=es_config['host'],
                 port=es_config['port'],
                 user=es_config['user'],
                 password=es_config['password'],
                 doc_type="_doc"):
        
        self._index = index
        self._conn = None
        self.__connect(
            host=host,
            port=port,
            http_auth=(user, password)
        )
        self._doc_type = doc_type

    def __connect(self, host, port, http_auth):
        """
        Connects to an Elasticsearch instance
        """
        self._conn = Elasticsearch(hosts=host, http_auth=http_auth, port=port)
        if self._conn.ping():
            print('ES conenction checking: Connected')
        else:
            print('ES conenction checking: Connection Error')

    def create_index(self, delete_if_exists=False):
        """
        Creates an index on the connected ES instance
        """

        try:
            if self._conn.indices.exists(self._index):
                # Delete index if existing
                if delete_if_exists:
                    self.delete_index()
                    self._conn.indices.create(index=self._index)
                    print('Created Index {}.'.format(self._index))
            else:
                self._conn.indices.create(index=self._index)
                print('Created Index {}.'.format(self._index))

        except Exception as ex:
            print(str(ex))

    def get_indices(self):
        indices_list = []
        for index in self._conn.indices.get('*'):
            if index != 'caching' and index!= 'annotations' and not index.startswith('.'):
                indices_list.append(index)
        return indices_list
    
    def get_current_index(self):
        return self._index

    def change_index(self, new_index, delete_if_exists=True):
        """
        Creates an index on the connected ES instance
        """
        self._index = new_index
    
    def delete_index(self):
        try:
            self._conn.indices.delete(index=self._index)
            print('Deleted Index {}.'.format(self._index))
        except Exception as ex:
            print(str(ex))

    def store_record(self, record, record_id):
        """
        :param record_id: ID (string) used for later accesses
        :param record: dictionary to be stored
        """
        try:
            if not self._conn.indices.exists(self._index):
                self._conn.indices.create(index=self._index)
                print('Created Index {}.'.format(self._index))
            self._conn.index(index=self._index, doc_type=self._doc_type, body=record, id=record_id)
            return 'okay'
        except Exception as ex:
            print('Error in indexing data.')
            print(str(ex))
            return 'Error in indexing data.'

    def store_record_to_index(self, record, record_id, es_index):
        """
        :param record_id: ID (string) used for later accesses
        :param record: dictionary to be stored
        """
        try:
            return self._conn.index(index=es_index, doc_type=self._doc_type, body=record, id=record_id, refresh='wait_for')
        except Exception as e:
            print('Error in store_record_to_index: ', str(e))
            return {}

    def store_record_withoutID(self, record, es_index):
        """
        :param record_id: ID (string) used for later accesses
        :param record: dictionary to be stored
        """
        try:
            return self._conn.index(index=es_index, doc_type=self._doc_type, body=record, refresh='wait_for')
        except Exception as ex:
            print('Error in store_record_withoutID: ', str(ex))
            return {}

    def get_record_from_index_by_id(self, record_id, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                "terms": {
                  "_id": [record_id]
                }
            }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            response = s.execute()
            if len(response.hits) < 1 :
                return None
            return response.hits[0].value

        except Exception as ex:
            print(str(ex))
    
    
    
    def get_record_from_index_by_list_of_ids(self, record_id, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                "terms" : {
                            "_id" : record_id
                        }
                }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            result = []
            # print('hehe', record_id)
            for hit in s.scan():
                return_obj = hit.to_dict()
                return_obj['record_id'] = hit.meta.id
                result.append(return_obj)
                # print('baba', hit.meta.id)
                # result.append(hit.to_dict())
            return result

        except Exception as ex:
            print(str(ex))

    def get_record_from_index_by_id_without_parsing_value(self, record_id, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                "terms": {
                  "_id": [record_id]
                }
            }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            response = s.execute()
            return response.hits[0].to_dict()

        except Exception as ex:
            print(str(ex))

    def get_all_records_from_index(self, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                    "match_all": {}
                }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            result = []
            for hit in s.scan():
                return_obj = hit.to_dict()['value']
                return_obj['record_id'] = hit.meta.id
                result.append(return_obj)
            return result

        except Exception as ex:
            print(str(ex))
    
    def get_record_from_index_by_search_string_in_name(self, search_value, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                    "query_string": {
                        "default_field" : "value.name",
                        "query" : "*"+search_value+"*"
                    }
            }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            result = []
            for hit in s.scan():
                return_obj = hit.to_dict()['value']
                return_obj['record_id'] = hit.meta.id
                result.append(return_obj)
            return result

        except Exception as ex:
            print(str(ex))
    
    def get_record_from_index_by_search_string_in_tag(self, search_value, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                    "query_string": {
                        "default_field" : "value.tag",
                        "query" : "*"+search_value+"*"
                    }
            }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            result = []
            for hit in s.scan():
                return_obj = hit.to_dict()['value']
                return_obj['record_id'] = hit.meta.id
                result.append(return_obj)
            return result

        except Exception as ex:
            print(str(ex))

    
    def get_record_by_userKey(self, userKey, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                "match_phrase": {
                  "userKey": userKey
                }
            }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            result = []
            for hit in s.scan():
                return_obj = hit.to_dict()
                return_obj['record_id'] = hit.meta.id
                result.append(return_obj)
            return result

        except Exception as ex:
            print(str(ex))
            print('Wrong in get record by userKey')
    
    
    def get_record_by_userKey_and_inferenceMode_and_ModelID(self, userKey, inferenceMode, es_index, activeModelID):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                    "bool": {
                        "must": 
                            [
                                {"match_phrase": {"userKey":  userKey}},
                                {"match_phrase": {"inferenceMode":  inferenceMode}},
                                {"match_phrase": {"baseModelID":  activeModelID}}
                            ]
                        }
                 }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            result = []
            for hit in s.scan():
                return_obj = hit.to_dict()
                return_obj['record_id'] = hit.meta.id
                result.append(return_obj)
            return result
        except Exception as ex:
            print(str(ex))
            print('Wrong in get record by userKey')


    def get_record_by_id(self, record_id):
        """
        Queries the connected ES instance by a certain id
        :param record_id: ID (string) used to access the required document.
        :return: response object
        """
        try:
            if not self._conn.indices.exists(self._index):
                self._conn.indices.create(index=self._index)
                print('Created Index {}.'.format(self._index))
            query = {
                "query": {
                "terms": {
                  "_id": [record_id]
                }
            }
            }
            s = Search(using=self._conn, index=self._index, doc_type=self._doc_type)
            s.update_from_dict(query)
            response = s.execute()
            return response.hits[0].value

        except Exception as ex:
            print(str(ex))
    
    def get_caching_record_by_id(self, record_id):
        """
        Queries the connected ES instance by a certain id
        :param record_id: ID (string) used to access the required document.
        :return: response object
        """
        try:
            if not self._conn.indices.exists(self._index):
                self._conn.indices.create(index=self._index)
                print('Created Index {}.'.format(self._index))
            query = {
                "query": {
                "terms": {
                  "_id": [record_id]
                }
            }
            }
            s = Search(using=self._conn, index=self._index, doc_type=self._doc_type)
            s.update_from_dict(query)
            response = s.execute()
            return response

        except Exception as ex:
            print(str(ex))
    
    def delete_record_from_index_by_id(self, record_id, es_index):
        try:
            self._conn.delete(index=es_index, doc_type=self._doc_type, id=record_id)
        except Exception as ex:
            print('Error in delete data.')
            print(str(ex))

    def delete_record_by_userKey(self, userKey, es_index):
        try:
            if not self._conn.indices.exists(es_index):
                self._conn.indices.create(index=es_index)
                print('Created Index {}.'.format(es_index))
            query = {
                "query": {
                "match_phrase": {
                  "userKey": userKey
                }
            }
            }
            s = Search(using=self._conn, index=es_index, doc_type=self._doc_type)
            s.update_from_dict(query)
            s.delete()

        except Exception as ex:
            print(str(ex))
            print('Wrong in delete record by userKey')
    
    
class CachingESConnection(ESConnection):

    def __init__(self,
                 index=elastic_index_config['es_index_caching'],
                 host=es_config['host'],
                 port=es_config['port'],
                 user=es_config['user'],
                 password=es_config['password'],
                 doc_type="_doc"):
        super().__init__(index, host, port, user, password, doc_type)
    
    def store_cache_elem(self, key, df, **kwargs):
        """
        Store the given df as cache entry.
        The other parameters are used as header.
        """
        record = {'timestamp': datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ'),
                  'key': key,
                  'values': json.dumps(df)}

        self.store_record(record_id=key, record=record)
    
    def get_cached_elem(self, key):
        """
        Retrieves and checks a cached element from the cache index.
        :return the cache entry as df if result is valid, otherwise return None
        """
        response = self.get_caching_record_by_id(key)
        if response.success():

            # compatibility with older elasticsearch versions
            try:
                response_length = response.hits.total.value
            except AttributeError:
                response_length = response.hits.total

            if response_length == 1:
                result = response.hits[0]
                return result.to_dict()['values']
            elif response.hits.total.value == 0:
                # print('No results in elasticsearch for {}.'.format(key))
                return None

            else:
                print('Multiple results for {}.'.format(key))
                return None
        else:
            print('Query for {} was not successful.'.format(key))
            return None
    
    def get_cached_elem_list(self, key):
        """
        Retrieves and checks a cached element from the cache index.
        :return the cache entry as df if result is valid, otherwise return None
        """
        response = self.get_record_from_index_by_list_of_ids(key, 'caching')
        return response
