import unittest
from app.models import User, Comments
from app import db

class TestPitchModel(unittest.TestCase):

  def setUp(self):
    self.current_user = User(username = 'jay', password = 'unclejj', email = 'jay@yahoo.com')
  
  def tearDown(self):
    db.session.delete(self)
    User.query.commit()

  def test_instance(self):
    self.assertTrue(isinstance(self.new_comment,Comments))