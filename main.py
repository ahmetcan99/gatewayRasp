import paho.mqtt.client as mqtt
import uvicorn
import threading
from fastapi import FastAPI
from restapi.routes import router
from mqtt_controller.config import BROKER, PORT
from mqtt_controller.mqtt_handler import on_connect, on_message
import ocr.ocr

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("can", "123456")

app = FastAPI(title="Gateway API")

app.include_router(router)

fastapi_thread = None
fastapi_server = None

def main():
    ocr_thread = threading.Thread(target=ocr.ocr.run, daemon=True)
    ocr_thread.start()

    global fastapi_thread

    start_mqtt()

    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()

    input("MQTT and REST API are running. Press Enter to exit...\n")
    stop_fastapi()
    stop_mqtt()
    print("Exiting...")

def start_fastapi():
    global fastapi_server
    fastapi_server = uvicorn.Server(uvicorn.Config(app, host="0.0.0.0", port=8000))
    fastapi_server.run()

def stop_fastapi():
    if fastapi_server:
        fastapi_server.should_exit = True
        print("FastAPI shutting down...")

def start_mqtt():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()

def stop_mqtt():
    client.loop_stop()
    client.disconnect()
    print("MQTT disconnected.")

if __name__ == "__main__":
    main()