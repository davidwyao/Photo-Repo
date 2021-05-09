import pyrebase
import requests
import time
import os

class firebase_controller:
    def __init__(self):
        self.config = {
        "apiKey": "AIzaSyBc2_kP4DurEZpX_poqEHJKdf1G1Vwa_Iw",
        "authDomain": "photorepo-42056.firebaseapp.com",
        "databaseURL": "https://photorepo-42056-default-rtdb.firebaseio.com/",
        "storageBucket": "photorepo-42056.appspot.com"
        }

        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()

        self.storage = self.firebase.storage()
        self.db = self.firebase.database()

        self.user = None
        self.email_name = None
        self.uploadpath = "../upload/"
        self.downloadpath = "../download/"

    def login(self, email, password):
        try:
            self.user = self.auth.sign_in_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            print("Error logging in: " + e.args[0].response.json()['error']['message'])
            return False
        
        self.email_name = email.split("@")[0]
        return True

    def signup(self, email, password):
        try:
            self.user = self.auth.create_user_with_email_and_password(email, password)
            self.email_name = email.split("@")[0]

            key = str(time.time()).replace(".", "")
            self.db.child("registered").child(self.email_name).set(key,self.user['idToken'])
        except requests.exceptions.HTTPError as e:
            print("Error registering: " + e.args[0].response.json()['error']['message'])
            return False

        return True

    def logout(self):
        self.user = None
        self.email_name = None

    def display_images(self, name):
        print(name + "'s images:")
        try:
            p_values = None
            values = None
            values = self.db.child("public").child(name).get(self.user['idToken']).each()
            if name == self.email_name:
                p_values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
        except requests.exceptions.HTTPError as e:
            print("Error connecting to database.")
        except:
            print("Error connecting to database.")
            return False

        if values is None and p_values is None:
            print("This user has no visible images.")
            return False

        if values is not None:
            print("PUBLIC:")
            for value in values:
                print(value.val())
        
        if p_values is not None:
            print("")
            print("PRIVATE:")
            for p_value in p_values:
                print(p_value.val())


        return True

    def upload(self, images, private):
        existing_images = []
        try:
            if private:
                values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
            else:
                values = self.db.child("public").child(self.email_name).get(self.user['idToken']).each()
        except requests.exceptions.HTTPError as e:
            print("Error connecting to database: " + e.args[0].response.json()['error']['message'])
            return
        
        if values is not None:
            for value in values:
                existing_images.append(value.val())

        for image in images:
            if image not in existing_images:
                print("Uploading " + image + "...", end = '')
                key = str(time.time()).replace(".", "")

                try:
                    if private:
                        self.storage.child(self.email_name).child("private/" + key).put(self.uploadpath + image, self.user['idToken'])
                        self.db.child("private").child(self.user['localId']).child(key).set(image,self.user['idToken'])
                    else:
                        self.storage.child(self.email_name).child("public/" + key).put(self.uploadpath + image, self.user['idToken'])
                        self.db.child("public").child(self.email_name).child(key).set(image,self.user['idToken'])
                except requests.exceptions.HTTPError as e:
                    print("Error uploading to database: " + e.args[0].response.json()['error']['message'])
                except:
                    print("Error uploading file.")
                else:
                    print("done")
                    existing_images.append(image)
            else:
                print("Image file " + image + " already exists.")

    def download_images(self, name, images, private):
        try:
            if private and name == self.email_name:
                values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
            elif not private:
                values = self.db.child("public").child(name).get(self.user['idToken']).each()
            else:
                print("Unauthorized operation.")
                return
        except requests.exceptions.HTTPError as e:
            print("Error connecting to database.")
            return
        if values is None:
            print("There are no visible images for this user.")
            return

        if self.create_directory(name):
            for value in values:
                if value.val() in images:
                    print("Downloading " + value.val() + "...", end = '')
                    try:
                        if not private:
                            self.storage.child(name).child("public/" + value.key()).\
                                download(self.downloadpath + name + "/public/", self.downloadpath\
                                    + name + "/public/" + value.val(), self.user['idToken'])
                        else:
                            self.storage.child(name).child("private/" + value.key()).\
                                download(self.downloadpath + name + "/private/", self.downloadpath\
                                    + name + "/private/" + value.val(), self.user['idToken'])
                    except requests.exceptions.HTTPError as e:
                        print("Error downloading from database.")
                    except:
                        print("Error downloading file.")
                    else:
                        print("done")

    def download_all(self, name):
        try:
            p_values = None
            values = self.db.child("public").child(name).get(self.user['idToken']).each()
            if name == self.email_name:
                p_values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
        except requests.exceptions.HTTPError as e:
            print("Error connecting to database.")
            return
        
        if self.create_directory(name):
            if values is not None:
                for value in values:
                    print("Downloading " + value.val() + "...", end = '')

                    try:
                        self.storage.child(name).child("public/" + value.key()).\
                            download(self.downloadpath + name + "/public/", self.downloadpath\
                                + name + "/public/" + value.val(), self.user['idToken'])
                    except requests.exceptions.HTTPError as e:
                        print("Error downloading from database.")
                    except:
                        print("Error downloading file.")
                    else:
                        print("done")

            if p_values is not None:
                for p_value in p_values:
                    print("Downloading private/" + p_value.val() + "...", end = '')
                    try:
                        self.storage.child(name).child("private/" + p_value.key()).\
                            download(self.downloadpath + name + "/private/", self.downloadpath\
                                + name + "/private/" + p_value.val(), self.user['idToken'])
                    except requests.exceptions.HTTPError as e:
                        print("Error downloading from database.")
                    except:
                        print("Error downloading file.")
                    else:
                        print("done")
        else:
            return

    def delete_images(self, images, private):
        # Files themselves can be deleted from firebase backend using cloud functions
        try:
            if private:
                values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
            else:
                values = self.db.child("public").child(self.email_name).get(self.user['idToken']).each()
        except requests.exceptions.HTTPError as e:
            print("Error connecting to database: " + e.args[0].response.json()['error']['message'])
            return

        for value in values:
            if value.val() in images:
                try:
                    if private:
                        self.db.child("private").child(self.user['localId']).child(value.key()).remove(self.user['idToken'])
                    else:
                        self.db.child("public").child(self.email_name).child(value.key()).remove(self.user['idToken'])
                except requests.exceptions.HTTPError as e:
                    print("Error deleting " + value.val() + "from database: " + e.args[0].response.json()['error']['message'])

    def delete_all(self):
        # Files themselves can be deleted from firebase backend using cloud functions
        try:
            self.db.child("private").child(self.user['localId']).remove(self.user['idToken'])
            self.db.child("public").child(self.email_name).remove(self.user['idToken'])
        except requests.exceptions.HTTPError as e:
            print("Error deleting key from database: " + e.args[0].response.json()['error']['message'])

    def create_directory(self, name):
        try:
            if not os.path.exists(self.downloadpath + name + "/public/") or not os.path.exists(self.downloadpath + name + "/private/"):
                os.makedirs(self.downloadpath + name + "/private/")
                os.mkdir(self.downloadpath + name + "/public/")
        except:
            print("Error creating download directory.")
            return False

        return True

    def get_email_name(self):
        return self.email_name

    def get_user(self):
        return self.user