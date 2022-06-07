import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from app.main.services.correlation_analysis import CorrelationAnalysis
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import *
from scipy import stats
import numpy as np
import time
from app.main.utils.data_transformation import array_to_df, df_to_dict, df_to_json
from app.main.utils.es_connection import ESConnection
from sys import getsizeof
import json
import ast
from flask import abort
es = ESConnection()
class DataGeneration(object):
    def __init__(self, userKey, df, selectedDimensions, all_aggregated_feature, threshold_configuration):
        self.es = es
        self.data = df
        self.userKey = userKey
        self.selectedDimensions = selectedDimensions
        self.samplingRate = threshold_configuration['samplingRate']
        self.all_aggregated_feature = all_aggregated_feature
        self.topics = self.data['topic'].unique()
    
    def generate_data_pairwise_row_id(self):
        try:
            start_time = time.time()
            # hard code id
            part_id = self.userKey
            # part_id = 'dang-study3test2/ban_nuclear_parsed_dus_infer.xml'
            record = self.es.get_record_from_index_by_id(part_id, 'training-data-ids')
            if record is not None:
                result_df = pd.DataFrame(json.loads(record))
                result_df.index = result_df.index.astype(int)
                return result_df
            else:
                print('--- Start generate_data_pairwise_row_id .....', flush=True)
                np.random.seed(1)
                result_df = pd.DataFrame()
                for top in self.topics:
                    data_per_topic = self.data[self.data['topic']==top].fillna(0)
                    data_per_topic = data_per_topic[data_per_topic['stance_WA'].astype(int)==1].reset_index()
                    print('--- Total data row: ', len(data_per_topic), flush=True)
                    if len(data_per_topic) > 150:
                        data_per_topic = data_per_topic.head(150)

                    learning_data = data_per_topic
                    index_list = learning_data.index.values
                    events_data = []
                    positives = index_list
                    negatives = index_list
                    # test without random choice
                    positives = np.random.choice(index_list, len(index_list))
                    negatives = np.random.choice(index_list, len(index_list))
                    for i in range(1,len(positives)):
                        for j in range(1,len(negatives)):
                            positive = positives[i]
                            negative = negatives[j]
                            e1 = [positive]
                            e2 = [negative]
                            label = 0
                            diff_pos_neg = float(data_per_topic.loc[positive, 'WA']) - float(data_per_topic.loc[negative, 'WA'])
                            if diff_pos_neg >0.05 and diff_pos_neg <= 0.25:
                                label = 1
                            elif diff_pos_neg > 0.25:
                                label = 2
                            elif diff_pos_neg < -0.05 and diff_pos_neg >= -0.25:
                                label = -1
                            elif diff_pos_neg < -0.25:
                                label = -2
                            else:
                                label = 0
                            pos_neg_example = np.concatenate([e1, e2, [label]])
                            events_data.append(pos_neg_example)
                    c1 = ['ind1']
                    c2 = ['ind2']
                    result =  pd.DataFrame(events_data, columns = np.concatenate([c1, c2, ['outcome']]))
                    result_df = pd.concat([result, result_df], ignore_index=True)
                
                result_df = result_df.sample(frac=1).reset_index(drop=True)
                # print('--- Class distribution: ', result_df['outcome'].value_counts(), flush=True)
                
                self.es.store_record_to_index({'value': json.dumps(result_df.to_dict())}, self.userKey, 'training-data-ids')

                print('--- Process generate_data_pairwise_row_id takes: ', time.time() - start_time, flush=True)
                return result_df
        except Exception as e:
            print('Error in generate_data_pairwise_row_id (data generation service): ', str(e), flush=True)
            abort(400, 'Error in generate_data_pairwise_row_id (data generation service): ' + str(e))
    
    def generate_event_data(self, df1, df2):
        try:
            ignored_features = ['MACE-P', 'WA', 'argument', 'stance_WA', 'topic']
            for agg_fea in self.all_aggregated_feature:
                if agg_fea['newDimensionName'] in self.selectedDimensions:
                    try:
                        print('--- Adding aggregated feature in generating event data: ', agg_fea['newDimensionName'])
                        df1 = self.add_aggregated_feature_to_df(df1, agg_fea['selectedDimensions'], agg_fea['convertDataTypeOption'], agg_fea['visualizationOption'],\
                            agg_fea['aggregationOption'], agg_fea['convertDataThreshold'], agg_fea['newDimensionName'], agg_fea['logicalOperatorsConfig'], agg_fea['customMathEquationConfig'])
                        df2 = self.add_aggregated_feature_to_df(df2, agg_fea['selectedDimensions'], agg_fea['convertDataTypeOption'], agg_fea['visualizationOption'], \
                            agg_fea['aggregationOption'], agg_fea['convertDataThreshold'], agg_fea['newDimensionName'], agg_fea['logicalOperatorsConfig'], agg_fea['customMathEquationConfig'])
                    except Exception as ex:
                        print('Error in adding aggregated feature generate_event_data (data generation service): ', str(ex), flush=True)
            
            # Filter the selected features for training data
            return pd.concat([df1.drop(columns=ignored_features)[self.selectedDimensions].add_suffix('_1').reset_index(drop=True), df2.drop(columns=ignored_features)[self.selectedDimensions].add_suffix('_2').reset_index(drop=True)], axis=1)
        except Exception as e:
            print('Error in generate_event_data (data generation service): ', str(e), flush=True)
            abort(400, 'Error in generate_event_data (data generation service): ' + str(e))

    def get_sample_data(self):
        try:
            start_time = time.time()
            train_index = []
            test_index = []
            row_id_data = self.generate_data_pairwise_row_id()
            sampling_rate_train = float(self.samplingRate)
            sampling_rate_test = 0.1
            if sampling_rate_train > 0.9: 
                sampling_rate_train = 0.9
            
            # hard-coded training data
            part_id = self.userKey 
            # part_id = 'dang.maitest2/ban_nuclear_parsed_dus_infer.xml'
            record_id = part_id + str(self.samplingRate)
            record = self.es.get_record_from_index_by_id(record_id, 'training-data-ids')
            if record is not None:
                re = json.loads(record)
                train_index = list(map(int, json.loads(re['train_index'])))
                test_index = list(map(int, json.loads(re['test_index'])))
            else:
                sss = StratifiedShuffleSplit(n_splits=1, train_size = int(sampling_rate_train * len(row_id_data)), test_size=int(sampling_rate_test * len(row_id_data)), random_state=42)
                for train_ind, test_ind in sss.split(row_id_data, row_id_data['outcome']):
                    train_index = train_ind
                    test_index = test_ind
                record_dict = dict()
                record_dict['train_index'] = json.dumps(list(map(str, train_index)))
                record_dict['test_index'] = json.dumps(list(map(str, test_index)))
                self.es.store_record_to_index({'value': json.dumps(record_dict)}, record_id, 'training-data-ids')
            
            train_data1 = self.data.loc[row_id_data.loc[train_index, 'ind1'].tolist()]
            train_data2 = self.data.loc[row_id_data.loc[train_index, 'ind2'].tolist()]
            test_data1 = self.data.loc[row_id_data.loc[test_index, 'ind1'].tolist()]
            test_data2 = self.data.loc[row_id_data.loc[test_index, 'ind2'].tolist()]
            arg_data = pd.concat([test_data1[['argument']].add_suffix('_1').reset_index(drop=True), test_data2[['argument']].add_suffix('_2').reset_index(drop=True)], axis=1) 
            X_train = self.generate_event_data(train_data1, train_data2)
            y_train = row_id_data.loc[train_index, 'outcome'].tolist()
            X_test = self.generate_event_data(test_data1, test_data2)
            y_test = row_id_data.loc[test_index, 'outcome'].tolist()
            
            # Normalize data
            transformer = RobustScaler().fit(pd.concat([X_train, X_test]))
            norm_train = transformer.transform(X_train)
            X_train = pd.DataFrame(norm_train, columns=X_train.columns, index=X_train.index)
            norm_test = transformer.transform(X_test)
            X_test = pd.DataFrame(norm_test, columns=X_test.columns, index=X_test.index)
            
            print('--- Process get_sample_data(data generation service) takes: ', time.time() - start_time, flush=True)
            return [X_train, X_test, y_train, y_test, X_test.index.values.tolist(), arg_data]
        except Exception as e:
            print('Error in get_sample_data (data generation service): ', str(e), flush=True)
            abort(400, 'Error in get_sample_data (data generation service): ' + str(e))

        
    
    def add_aggregated_feature_to_df(self, result_df, selectedDimension, convertDataTypeOption, visualizationOption, aggregationOption, convertDataThreshold, newDimensionName, logicalOperatorsConfig, customMathEquationConfig):
        corrAna = CorrelationAnalysis()
        return_df = pd.DataFrame()
        newSelectedDimensionName = []
        all_cols =  result_df.columns
        for feature in selectedDimension:
            name_col = feature
            if name_col in all_cols:
                newSelectedDimensionName.append(name_col)
        if convertDataTypeOption == 'binary':
            return_df = corrAna.binary_aggregation(result_df, newSelectedDimensionName, 'keep', aggregationOption, convertDataThreshold, newDimensionName, logicalOperatorsConfig)
        elif convertDataTypeOption == 'numerical':
            return_df = corrAna.numerical_aggregation(result_df, newSelectedDimensionName, 'keep', aggregationOption, newDimensionName, customMathEquationConfig)
        return return_df
