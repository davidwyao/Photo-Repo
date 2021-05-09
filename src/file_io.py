from firebase_controller import firebase_controller

class file_io:
    def __init__(self, server_io):
        self.server_io = server_io
        self.valid_exts = ["jpg", "jpeg", "png", "gif", "bmp", "eps",\
            "tif", "tiff", "raw"]

    def prompt_activity(self):
        print("")
        self.display_images(self.server_io.get_email_name())
        while True:
            print("")
            selection = input("Enter 'l' to list any user's images.\n"
                "Enter 'u' to upload images.\n"
                "Enter 'd' to download images.\n"
                "Enter 'delete' to delete images.\n"
                "Enter 'x' to exit: ")
            
            if selection == "l":
                target_user = input("Enter the user whose images you want to view (@ to exit): ")
                if target_user == "@":
                    continue
                print("")
                self.display_images(target_user)

            elif selection == "u":
                self.prompt_upload()

            elif selection == "d":
                self.prompt_download()

            elif selection == "delete":
                self.prompt_delete()

            elif selection == "x":
                break 

            else:
                print("Invalid input!")
                continue

    def prompt_upload(self):
        while True:
            print("")
            files = []
            privacy = input("Who do you want to see your upload?\n"
                "Enter 'private' for a private upload.\n"
                "Enter 'public' for a public upload.\n"
                "Enter 'x' to exit: ")
            
            if privacy not in ["private", "public", "x"]:
                print("Invalid input!")
                continue

            if privacy == "x":
                return
            
            files = []
            print("")
            while True:
                file = input("Image to upload (enter 'done' when finished): ")

                if file == "done":
                    break

                elif file.split(".")[-1] not in self.valid_exts:
                    print(file + " is not one of: " + " ".join(self.valid_exts))
                    continue

                files.append(file)

            if privacy == "public":
                self.upload(files, False)
            else:
                self.upload(files, True)

        

    def prompt_download(self):
        while True:
            print("")
            target_user = input("Which user would you like to download from? (@ to exit): ")

            if target_user == "@":
                break
            
            files = []
            private_files = []
            print("")
            if not self.display_images(target_user):
                continue
            print("")

            while True:
                print("")
                file = input("Enter the image name to download.\n"
                    "Prefix private images with 'p/'.\n"
                    "Enter 'all' to download everything.\n"
                    "Enter 'done' when finished: ")

                if file == "done":
                    break
                elif file == "all":
                    self.download_all(target_user)
                    break
                else:
                    if file[:2] != "p/":
                        files.append(file)
                    else:
                        private_files.append(file.split("/")[1])

            self.download_images(target_user, files, False)
            if private_files != []:
                self.download_images(target_user, private_files, True)

    def prompt_delete(self):
        files = []
        while True:
            print("")
            self.display_images(self.server_io.get_email_name())
            print("")

            selection = input("Delete from your public, private, or all repositories?\n"
                "Enter 'public' to delete a public image.\n"
                "Enter 'private' to delete a private image.\n"
                "Enter 'all' to delete all of your images!\n"
                "Enter 'x' to exit: ")

            if selection not in ["public", "private", "all", "x"]:
                print("Invalid input!")
                continue

            elif selection == "all":
                self.delete_all()

            elif selection == "x":
                break

            else:
                print("")
                while True:
                    file = input("Image to delete (enter 'done' when finished): ")
                    if file == "done":
                        break
                    files.append(file)
                if selection == "public":
                    self.delete_images(files, False)
                else:
                    self.delete_images(files, True)

    def display_images(self, name):
        return self.server_io.display_images(name)

    def upload(self, images, private):
        self.server_io.upload(images, private)

    def download_images(self, name, images, private):
        self.server_io.download_images(name, images, private)

    def download_all(self, name):
        self.server_io.download_all(name)

    def delete_images(self, images, private):
        self.server_io.delete_images(images, private)

    def delete_all(self):
        self.server_io.delete_all()