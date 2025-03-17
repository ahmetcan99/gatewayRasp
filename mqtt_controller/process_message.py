import json
import uuid
import time
import paho.mqtt.client as mqtt
from .config import BROKER, PORT, USER_NAME, PASSWORD, image_save_dir
from db import models

class Process_Message:
    def process_message(self, client, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))

            # topic_parts = msg.topic.split('/')
            
            # if len(topic_parts) >= 3 and topic_parts[0] == "esp32":
            #     camera_uuid = topic_parts[1]

            #     photo_uuid = str(uuid.uuid4())

            #     file_name = f"{photo_uuid}_{camera_uuid}.jpg"

            #     current_date = datetime.now()

            #     date_folder = current_date.strftime("%Y-%m-%d")

            #     file_path = os.path.join(image_save_dir, date_folder)
                
            #     if not os.path.exists(file_path):
            #         os.makedirs(file_path)
                
            #     with open(file_path, "wb") as image_file:
            #        image_file.write(msg.payload)

            #     print(f"Photo saved as {file_name}")
            # else:
            #     print("Invalid topic format")


                
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