from flask import Blueprint
import toolz as t

from app.db.models.device import Device
from app.db.models.interaction import Interaction
from app.db.repository.device_repository import insert_device
from app.db.repository.interaction_repository import insert_interaction

phone_blueprint = Blueprint("phone_tracker", __name__)

from flask import jsonify, request


@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   try:
      data = request.json
      if not data:
         return jsonify({"error": "No data provided"}), 400

      devices = data['devices']
      interaction = data['interaction']
      devices_models = t.pipe(
         devices,
         t.partial(map, lambda d: insert_device(Device(**d))),
         list
      )
      interaction_model = t.pipe(
         interaction,
         lambda i: insert_interaction(Interaction(**i))
      )
      return jsonify({"message": "Devices and interaction processed successfully"}), 200

   except Exception as e:
      print(str(e))
      return jsonify({"error": f"Unexpected error: {str(e)}"}), 500




@phone_blueprint.route("/api/bluetooth_connection", methods=['GET'])
def get_bluetooth_interaction():
   try:
