import pyrebase

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
            self.email_name = email.split("@")[0]
        except:
            return False
        
        return True

    def signup(self, email, password):
        try:
            self.user = self.auth.create_user_with_email_and_password(email, password)
            self.email_name = email.split("@")[0]
        except:
            return False

        try:
            self.db.child("users").child(self.email_name).child("private").push("default.png")
            self.storage.child(self.email_name).child("private/default.png").put("../upload/default.png", self.user['idToken'])
        except:
            print("Could not connect to server!")
            return False

        return True

    def signout(self):
        self.user = None
        self.email_name = None

    def upload(self, images, private):
        if private:
            for image in images:
                try:
                    print("Uploading " + image)
                    self.storage.child(self.email_name).child("private/" + image).put(self.uploadpath + image, self.user['idToken'])
                    self.db.child("users").child(self.email_name).child("private").push(image)
                except:
                    print("Invalid image " + image)
        else:
            for image in images:
                try:
                    print("Uploading " + image)
                    self.storage.child(self.email_name).child("public/" + image).put(self.uploadpath + image, self.user['idToken'])
                    self.db.child("users").child(self.email_name).child("public").push(image)
                except:
                    print("invalid image " + image)

    def download_all(self, name):
        values = self.db.child("users").child(name).child("public").get().each()
        
        for value in values:
            print(value.val())
            self.storage.child(name).child("public/" + value.val()).\
                download(self.downloadpath, self.downloadpath + value.val(), self.user['idToken'])

        values = []
        if name == self.email_name:
            values = values + self.db.child("users").child(name).child("private").get().each()
            for value in values:
                print("private/" + value.val())
                self.storage.child(name).child("private/" + value.val()).\
                    download(self.downloadpath, self.downloadpath + value.val(), self.user['idToken'])