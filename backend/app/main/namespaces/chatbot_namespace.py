from flask import jsonify, abort
from flask_restplus import Resource
from flask_restplus import Namespace
from flask import request
import json
import ast
from app.main.controllers.chatbot_controller import ChatBotController
from app.main.utils.data_transformation import df_to_dict, df_to_json, string_to_df
import time
api = Namespace('chat-bot', description="Operations retrieving chatbot data"
                                       "(e.g., ).")

chatbot_controller = ChatBotController()
@api.route('/get_chat_history_data')
class GetChatHistoryData(Resource):
    @api.doc('get chat history data')
    @api.expect(chatbot_controller.parser)
    def post(self):
        """List all available entities, their features, and their time ranges."""
        try:
            userKey = request.json['userKey']
            temp_chatbot_controller = ChatBotController()
            result = temp_chatbot_controller.get_chat_history_data(userKey)
            return result
        except Exception as e:
            print('Error in request GetChatHistoryData: ', str(e), flush=True)
            abort(400, 'Error in request GetChatHistoryData: ' + str(e))

@api.route('/update_chat_history_data')
class UpdateChatHistoryData(Resource):
    @api.doc('update_chat_history_data')
    @api.expect(chatbot_controller.parser)
    def post(self):
        """List all available entities, their features, and their time ranges."""
        try:
            userKey = request.json['userKey']
            chat_history_data = request.json['chatHistoryData']
            temp_chatbot_controller = ChatBotController()
            return temp_chatbot_controller.update_chat_history_data(userKey, chat_history_data)
        except Exception as e:
            print('Error in request UpdateChatHistoryData: ', str(e), flush=True)
            abort(400, 'Error in request UpdateChatHistoryData: ' + str(e))