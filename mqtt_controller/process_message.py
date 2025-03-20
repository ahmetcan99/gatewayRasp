import json
import uuid
import time
from db import models

class Process_Message:
    def process_message(self, client, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))            
            msg_type = payload.get("type")
            if msg_type == "request":
                self.process_request(client, payload)

        except Exception as e:
            print(f"Error processing message : {e}")
            
    def process_request(self, client, payload):
        time.sleep(15)
        meter_mac = payload.get("client_id")
        description = payload.get("description")
        is_registered = models.get_meter_uuid_with_mac(meter_mac)

        if(is_registered != None):
            new_uuid = is_registered

            response_payload = {
            "type": "client_response",
            "client_id": meter_mac,
            "uuid": new_uuid,
            "message": "UUID founded, send back succesfully."
            }
            client.publish("esp32/uuid_exchange", json.dumps(response_payload))
        else:
            new_uuid = str(uuid.uuid4())
            response_payload = {
            "type": "client_response",
            "client_id": meter_mac,
            "uuid": new_uuid,
            "message": "UUID created, send back succesfully."
            }
            client.publish("esp32/uuid_exchange", json.dumps(response_payload))
            models.add_new_meter(new_uuid, meter_mac, description)
            print(f"UUID {new_uuid} assigned to device {payload.get('client_id')}")