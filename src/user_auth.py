from firebase_controller import firebase_controller

class user_auth:
    def __init__(self, server_io):
        self.server_io = server_io

    def prompt_login(self):
        while True:
            action = input("Login or register? (L/R): ")
            if action != "L" and action != "R":
                print("Invalid action! Please enter L or R.")
                continue

            username = input("Please enter your email: ")
            password = input("Please enter your password: ")

            if action == "L":
                if self.login(username, password):
                    break
                else:
                    print("Login failed!")
            elif action == "R":
                if self.signup(username, password):
                    break
                else:
                    print("Registration failed!")

    def login(self, email, password):
        return self.server_io.login(email, password)

    def signup(self, email, password):
        return self.server_io.signup(email, password)

    def signout(self):
        self.server_io.signout()