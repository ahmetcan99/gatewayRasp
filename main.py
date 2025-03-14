import paho.mqtt.client as mqtt
from mqtt_controller.config import BROKER, PORT
from mqtt_controller.mqtt_handler import on_connect, on_message

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("can", "123456")

def main():
    client.on_connect = on_connect
    client.on_message = on_message
    start_mqtt()
    input("MQTT is working, press Enter to exit..")
    stop_mqtt()
    print("Exiting...")


def start_mqtt():
    client.connect(BROKER, PORT, 60)
    client.loop_start()

def stop_mqtt():
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()