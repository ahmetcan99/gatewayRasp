from .process_message import Process_Message
from .config import TOPIC


process = Process_Message()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("")
        print("[MQTT] Connection is successfull.")
        client.subscribe(TOPIC)
    else:
        print(f"[MQTT] Connection failed. Error Code: {rc}")

def on_message(client, userdata, msg):
    try:
        process.process_message(client, msg)
    except Exception as e:
        print(f"[MQTT] Error: {e}")

