from app.models import Comments
from wtforms.validators import Required
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm


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
    opinion = TextAreaField('Write a your comment here...')
    submit = SubmitField('POST')

class PitchForm(FlaskForm):
    """
    Pitch Class to create a wtf-form for creating a pitch
    """
    pitch_title = StringField('Your Pitch title',validators=[Required()])
    pitch_category = SelectField('Pitch Categories', choices = [('Select the category','Select the pitch category'),('pickup','Pickup-lines'),('interview', 'Interview'), ('product', 'Product'),('promotion','Promotion')], validators=[Required()])
    pitch_comment = TextAreaField('Your Pitch')
    submit = SubmitField('Post Pitch')



