import unittest
from app.models import User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(username='ajaylee', password = 'jay')

    def test_password_setter(self):
        self.assertTrue(self.new_user.password_hash is None)

    def test_no_access_password(self):
            with self.assertRaises(AttributeError):
                self.new_user.password

    def test_password_verification(self):
            self.assertTrue(self.new_user.verify_password('jay'))

    def tearDown(self):
        user = User.query.filter_by(username="ajaylee").first()
        if user:
            print("password confirmed")        