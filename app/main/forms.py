from app.models import Comments
from wtforms.validators import Required
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm

class PitchForm(FlaskForm):
    """
    Pitch Class to create a wtf-form for creating a pitch
    """
    content = TextAreaField('INPUT YOUR PITCH')
    submit = SubmitField('SUBMIT')

class CategoryForm(FlaskForm):
    """
     Category Class to create a wtf-form for creating a pitch
    """
    name =  StringField('Category Name', validators=[Required()])
    submit = SubmitField('Create')

class CommentForm(FlaskForm):
    """
     Comment Class to create a wtf-form for creating a pitch
    """
    Comment = TextAreaField('WRITE A COMMENT')
    submit = SubmitField('SUBMIT')

