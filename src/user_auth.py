from firebase_controller import firebase_controller

class user_auth:
    def __init__(self, server_io):
        self.server_io = server_io

    def prompt_login(self):
        while True:
            print("")
            self.logout()
            action = input("Welcome!\n"
                "Enter 'l' to login.\n"
                "Enter 'r' to register.\n"
                "Enter 'x' to exit: ")

            if action not in ["l", "r", "x"]:
                print("Invalid input!")
                continue

            if action == "x":
                return False

            username = input("Please enter your email: ")
            password = input("Please enter your password: ")

            if action == "l":
                if self.login(username, password):
                    return True
                else:
                    print("Login failed!")

            elif action == "r":
                if self.signup(username, password):
                    return True
                else:
                    print("Registration failed!")

    def login(self, email, password):
        return self.server_io.login(email, password)

    def signup(self, email, password):
        return self.server_io.signup(email, password)

    def logout(self):
        self.server_io.logout()