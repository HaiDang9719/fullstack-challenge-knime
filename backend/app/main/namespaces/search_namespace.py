from flask import jsonify, abort
from flask_restplus import Resource
from flask_restplus import Namespace
from flask import request
import json
import ast
from app.main.controllers.search_controller import SearchController
from app.main.utils.data_transformation import df_to_dict, df_to_json
import time
api = Namespace('search', description="Operations retrieving node data"
                                       "(e.g., ).")

search_controller = SearchController()
@api.route('/get_all_node_info')
class GetAllNodeData(Resource):
    @api.doc('get_all_node_data')
    def post(self):
        """List all nodes"""
        try:
            temp_search_controller = SearchController()
            result = temp_search_controller.get_node_information_data()
            return result
        except Exception as e:
            print('Error in request GetAllNodeData: ', str(e), flush=True)
            abort(400, 'Error in request GetAllNodeData: ' + str(e))

@api.route('/get_top_nodes')
class GetTopNodeData(Resource):
    @api.doc('get_top_nodes')
    def post(self):
        """List all nodes"""
        try:
            temp_search_controller = SearchController()
            result = temp_search_controller.get_top_nodes()
            return result
        except Exception as e:
            print('Error in request GetTopNodeData: ', str(e), flush=True)
            abort(400, 'Error in request GetTopNodeData: ' + str(e))

@api.route('/search_node')
class SearchNodeByValue(Resource):
    @api.doc('search_node_by_value')
    def post(self):
        """Search node by values"""
        try:
            temp_search_controller = SearchController()
            search_value = request.json['searchValue']
            result = temp_search_controller.search_node_by_value(search_value)
            return result
        except Exception as e:
            print('Error in request SearchNodeByValue: ', str(e), flush=True)
            abort(400, 'Error in request SearchNodeByValue: ' + str(e))

@api.route('/add_new_node')
class AddNewNodeByValue(Resource):
    @api.doc('add_new_node')
    def post(self):
        """Add new nodes"""
        try:
            temp_search_controller = SearchController()
            nodeInfo = request.json['nodeInfo']
            result = temp_search_controller.add_node_information_data(nodeInfo)
            return result
        except Exception as e:
            print('Error in request AddNewNodeByValue: ', str(e), flush=True)
            abort(400, 'Error in request AddNewNodeByValue: ' + str(e))

@api.route('/update_node_info')
class UpdateNodeInfor(Resource):
    @api.doc('update_node_info')
    def post(self):
        """Update node information"""
        try:
            temp_search_controller = SearchController()
            nodeInfo = request.json['nodeInfo']
            recordID = request.json['recordID']
            result = temp_search_controller.update_node_information_data(nodeInfo, recordID)
            return result
        except Exception as e:
            print('Error in request UpdateNodeInfor: ', str(e), flush=True)
            abort(400, 'Error in request UpdateNodeInfor: ' + str(e))

@api.route('/delete_node_info')
class UpdateNodeInfor(Resource):
    @api.doc('delete_node_info')
    def post(self):
        """Delete node information"""
        try:
            temp_search_controller = SearchController()
            recordID = request.json['recordID']
            result = temp_search_controller.delete_node_information_data(recordID)
            return result
        except Exception as e:
            print('Error in request UpdateNodeInfor: ', str(e), flush=True)
            abort(400, 'Error in request UpdateNodeInfor: ' + str(e))