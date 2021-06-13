import unittest
from app.models import Comments


class CommentModelTest(unittest.TestCase):
    """
    Test Class to test the behaviour of the Comment class
    """

    def setUp(self):
        """
        Set up method that will run before every Test
        """
        self.comment= Comments(opinion = 'testing testing')


    def tearDown(self):
        Comments.query.delete()


    def test_instance(self):
        self.assertTrue(isinstance(self.comment, Comments))


    def test_check_instance_variables(self):
        self.assertEquals(self.comment.opinion,'testing testing')