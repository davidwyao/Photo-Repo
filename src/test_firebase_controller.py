import unittest
import os
from firebase_controller import firebase_controller

class firebase_test(unittest.TestCase):
    def setUp(self):
        self.server_io = firebase_controller()
        self.db = self.server_io.firebase.database()
        self.user = None

    def test_login(self):
        self.assertEqual(self.server_io.login("pytest@pytest.com", "pytest"), True, "user pytest has email pytest")
        self.assertEqual(self.server_io.login("pytest2@pytest.com", "pytest"), False, "user pytest2 does not exist")
        self.assertEqual(self.server_io.login("pytest2pytestcom", "pytest"), False, "invalid email")

    def test_signup(self):
        self.assertEqual(self.server_io.signup("pytest@pytest.com", "pytest"), False, "user pytest already registered")
        self.assertEqual(self.server_io.signup("pytest2pytestcom", "pytest"), False, "invalid email")

    def test_display_images(self):
        self.server_io.display_images("pytest")
        self.server_io.login("pytest@pytest.com", "pytest")
        self.assertEqual(self.server_io.display_images("pytest"), True, "logged-in viewing and has images")

    def test_upload(self):
        self.server_io.login("pytest@pytest.com", "pytest")
        self.user = self.server_io.get_user()

        image = ["pytest.jpg"]
        self.server_io.upload(image, True)
        uploaded = False
        p_values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
        for p_value in p_values:
            if p_value.val() in image:
                uploaded = True
        self.assertEqual(uploaded, True, "image uploaded successfully")

        image = ["garblgarbl.png"]
        self.server_io.upload(image, True)
        uploaded = False
        p_values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
        for p_value in p_values:
            if p_value.val() in image:
                uploaded = True
        self.assertEqual(uploaded, False, "nonexistent image not uploaded")

    def test_download_images(self):
        self.server_io.login("pytest@pytest.com", "pytest")
        self.user = self.server_io.get_user()
        
        images = ["patty2.jpg"]
        self.server_io.download_images("pytest",images,False)
        self.assertEqual(os.path.exists("../download/pytest/public/patty2.jpg"), True, "file downloaded into correct directory")

        images = ["catat.jpg"]
        self.server_io.download_images("dahvied0227",images,True)
        self.assertEqual(os.path.exists("../download/dahvied0227/private/catat.jpg"), False, "cannot access other user's private files")

        images = ["pat.jpg"]
        self.server_io.download_images("dahvied0227",images,False)
        self.assertEqual(os.path.exists("../download/dahvied0227/public/pat.jpg"), True, "can access other user's public files")

        os.remove("../download/pytest/public/patty2.jpg")
        os.remove("../download/dahvied0227/public/pat.jpg")

    def test_delete_images(self):
        self.server_io.login("pytest@pytest.com", "pytest")
        self.user = self.server_io.get_user()

        image = ["pytest.jpg"]
        self.server_io.delete_images(image, True)
        deleted = False
        p_values = self.db.child("private").child(self.user['localId']).get(self.user['idToken']).each()
        for p_value in p_values:
            if p_value.val() in image:
                deleted = True

        self.assertEqual(deleted, False, "image successfully deleted from record")

if __name__ == '__main__':
    unittest.main()