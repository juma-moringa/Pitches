from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    """
    @login_manager.user_loader Passes in a user_id to this function and in return the
    function queries the database and gets a user's id as a response...
    """
    return User.query.get(int(user_id))


# 1. USER CLASS
class User(UserMixin, db.Model):
    """ 
    class modelling the users 
    """

    __tablename__ = 'users'

    # creation of the  user columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship("Pitch", backref="user", lazy="dynamic")
    comment = db.relationship("Comments", backref="user", lazy="dynamic")
    vote = db.relationship("Votes", backref="user", lazy="dynamic")

    #  function for securing the users passwords

    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'

# 2. class pitches


class Pitch(db.Model):
    """
    Class pitch is a class that lists of pitches in each category.
    """

    __tablename__ = 'pitches'

    # id = db.Column(db.Integer,primary_key = True)
    # content = db.Column(db.String())
    # category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    # user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    id = db.Column(db.Integer, primary_key=True)
    pitch_id = db.Column(db.Integer)
    pitch_title = db.Column(db.String)
    pitch_category = db.Column(db.String)
    pitch_comment = db.Column(db.String)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    comment = db.relationship("Comments", backref="pitches", lazy="dynamic")
    vote = db.relationship("Votes", backref="pitches", lazy="dynamic")

    def save_pitch(self):
        """
        Save the pitches 
        """
        db.session.add(self)
        db.session.commit()

    # displaying of pitches

    @classmethod
    def get_pitches(cls, category):
        pitches = Pitch.query.filter_by(pitch_category=category).all()
        return pitches

    @classmethod
    def getPitchId(cls, id):
        pitch = Pitch.query.filter_by(id=id).first()
        return pitch


# 3. CLASS COMMENT
class Comments(db.Model):
    """
    Comments Class comment is model for each pitch 
    """

    __tablename__ = 'comments'

    # adding columns for our comments
    id = db.Column(db. Integer, primary_key=True)
    opinion = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
        """
        Save the Comments as per every pitch idea

        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(
            )
        return comment


# 4. CLASS CATEGORY
class Category(db.Model):

    __tablename__ = 'categories'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    # saving pitches
    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = Category.query.all()
        return categories

# 5. VOTES CLASS


class Votes  (db.Model):
    """
    Class votes is a class which  will be used to create the upvotes and downvotes for the pitches
    """
    __tablename__ = 'votes'

    id = db.Column(db. Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls, user_id, pitches_id):
        votes = Votes.query.filter_by(
            user_id=user_id, pitches_id=pitches_id).all()
        return votes

    def __repr__(self):
        return f'{self.vote}:{self.user_id}:{self.pitches_id}'

class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)        
