from firebase_controller import firebase_controller

class file_io:
    def __init__(self, server_io):
        self.server_io = server_io

    def prompt_upload(self):
        files = []
        while True:
            file = input("Public file to input (exit to exit):")
            if file == "exit":
                break
            files.append(file)
        self.upload(files, False)
        files = []
        while True:
            file = input("Private file to input (exit to exit):")
            if file == "exit":
                break
            files.append(file)
        self.upload(files, True)

    def prompt_download(self):
        while(True):
            target_user = input("Which email would you like to download from? (@ to exit):")
            if target_user == "@":
                break
            self.download_all(target_user)

    def upload(self, files, private):
        self.server_io.upload(files, private)

    def download_all(self, name):
        self.server_io.download_all(name)