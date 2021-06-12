from wtforms.validators import Required, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from flask_wtf import FlaskForm
from ..models import User


class RegistrationForm(FlaskForm):
    """
    RegstrationForm class that passes in the required details for validation
    """

    email = StringField('your email address', validators=[Required(), Email()])
    username = StringField('your username', validators=[Required()])
    password = PasswordField('password', validators=[Required(), EqualTo('password',message='passwords must be the same.')])
    password_confirm = PasswordField('confirm password', validators=[Required()])
    submit = SubmitField('sign Up')


    #custom validators(validate_email,validate_username)
    def validate_email(self, data_field):
        """
        Function which takes in the data field and checks our database to confirm user Validation
        """
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('There is an  already existing account with that email')


    def validate_username(self, data_field):
        """
        Function which checks if the username is unique and raises ValidationError
        """
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('OOOPS!!!!! That user name is already taken. Try another one')


#login class which takes three inputs from the user
class LoginForm(FlaskForm):
    email = StringField('Your email address', validators=[Required(),Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')



