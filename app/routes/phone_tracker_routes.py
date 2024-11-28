from crypt import methods

from flask import Blueprint, request, jsonify

phone_blueprint = Blueprint("phone_tracker", __name__)


@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   data = request.json




   return jsonify({ }), 200





@phone_blueprint.route("/api/bluetooth_connection", methods=['GET'])
def get_bluetooth_interaction():
   try:
