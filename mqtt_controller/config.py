import os

BROKER = "localhost"
PORT = 1883
TOPIC = "#"
USER_NAME = "control"
PASSWORD = "123456"

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
image_save_dir = os.path.join(current_dir,
                "common/new_images")

print(current_dir)
print(parent_dir)
print(image_save_dir)