import sys
sys.path.insert(0, './')

from firebase_controller import firebase_controller
from user_auth import user_auth
from file_io import file_io

server_interface = firebase_controller()
user_auth = user_auth(server_interface)
file_io = file_io(server_interface)

while(True):
    if not user_auth.prompt_login():
        break
    file_io.prompt_activity()

print("Exiting program.")
exit()