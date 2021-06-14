from app.models import Comment,User,Pitch
import unittest
from app import db


class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Peris = User(username = 'ajaylee',password = 'jay', email = 'littlej@gmail.com')
        

    def tearDown(self):
        User.query.delete()
        Pitch.query.delete()
      

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.pitch_title,'Test')
        self.assertEquals(self.new_pitch.pitch_content,'This is a test pitch')
        self.assertEquals(self.new_pitch.category,"PICK UP LINES")
        self.assertEquals(self.new_pitch.user,self.user_Peris)

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_pitch_by_id(self):
        self.new_pitch.save_pitch()
        got_pitch = Pitch.get_pitch(1)
        self.assertTrue(got_pitch is not None)