# backend/routes/api_routes.py

from flask import Blueprint, jsonify, request
from services.app_service import get_data, update_data, add_process, remove_process, edit_status, get_raw_data


api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return 'Flask is running - RunnerApp !'

@api_bp.route('/get-data/<type>', methods=['GET'])
def get_data_route(type):
    print(get_data(type))
    return jsonify(get_data(type))

@api_bp.route('/get-raw-data', methods=['GET'])
def get_raw_data_route():
    return get_raw_data()

@api_bp.route('/update-data', methods=['GET'])
def update_data_route():
    return jsonify(update_data())

@api_bp.route('/add-process', methods=['POST'])
def add_process_route():
    return add_process(request.json)

@api_bp.route('/remove-process', methods=['POST'])
def remove_process_route():
    return remove_process(request.json)

@api_bp.route('/edit-status', methods=['POST'])
def edit_status_route():
    return edit_status(request.json[0])
