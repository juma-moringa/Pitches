from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . forms import PitchForm, CommentForm, CategoryForm
from .import main
from .. import db
from ..models import User, Pitch, Comments,Category, Votes

#display categories on the landing page
@main.route('/')
def index():
    """

    View root page function that returns index page

    """

    all_category = Category.get_categories()
    all_pitches = Pitch.query.order_by('id').all()
    print(all_pitches)

    title = 'Pitchmentation254'
    return render_template('index.html', title = title, categories=all_category, all_pitches=all_pitches)


#Route for adding a newly created pitch
@main.route('/pitch/newpitch',methods= ['POST','GET'])
@login_required
def new_pitch():
    pitch = PitchForm()
    if pitch.validate_on_submit():
        title = pitch.pitch_title.data
        category = pitch.pitch_category.data
        yourPitch = pitch.pitch_comment.data

        #update pitch instance

        newPitch = Pitch(pitch_title = title,pitch_category = category,pitch_comment = yourPitch,user= current_user)

        #save pitch
        newPitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'pitched pitch'
    return render_template('pitchment.html',title = title,pitchform = pitch) 

     #functions to display the pitches categories and information.
@main.route('/category/pickup',methods= ['POST','GET'])
def display_pickup_category():
    pickupPitches = Pitch.get_pitches('pickup')
    return render_template('display/pickup.html',pickupPitches = pickupPitches)    

@main.route('/category/interview',methods= ['GET'])
def display_interview_category():
    interviewPitches = Pitch.get_pitches('interview')
    return render_template('display/interview.html',interviewPitches = interviewPitches)
    
@main.route('/category/product',methods= ['POST','GET'])
def display_product_category():
    productPitches = Pitch.get_pitches('product')
    return render_template('display/prod.html',productPitches = productPitches)

@main.route('/category/promotion',methods= ['POST','GET'])
def display_promotion_category():
    promotionPitches = Pitch.get_pitches('promotion')
    return render_template('display/promo.html',promotionPitches = promotionPitches)


@main.route('/categories/<int:id>')
def category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)

    pitches=Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)


@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    """
    View new category route function that returns a page with a form to create a category
    """
    
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name = name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title = 'Categories'
    return render_template('new_category.html', category_form = form, title = title)


#view single pitch with its comments
@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    """
    View_function is a function that returns a single pitch for a comment to be added
    """
    all_category = Category.get_categories()
    pitches = Pitch.query.get(id)
    

    if pitches is None:
        abort(404)
    
    comment = Comments.get_comments(id)
    count_likes = Votes.query.filter_by(pitches_id=id, vote=1).all()
    count_dislikes = Votes.query.filter_by(pitches_id=id, vote=2).all()
    return render_template('view-pitch.html', pitches = pitches, comment = comment, count_likes=len(count_likes), count_dislikes=len(count_dislikes), category_id = id, categories=all_category)



#adding a new comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    """ 

    Function to post a newly created comments 
    """
    
    form = CommentForm()
    title = 'Update comment'
    pitches = Pitch.query.filter_by(id=id).first()

    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion = opinion, user_id = current_user.id, pitches_id = pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id = pitches.id))

    return render_template('post_comment.html', comment_form = form, title = title)


#Routes for liking/dislike pitches
@main.route('/pitch/upvote/<int:id>&<int:vote_type>')
@login_required
def upvote(id,vote_type):
    """
    View function that adds one to the vote_number column in the table
    """
    # Query for  the user
    votes = Votes.query.filter_by(user_id=current_user.id).all()
    # print(f'The new vote is {votes}')
    to_str=f'{vote_type}:{current_user.id}:{id}'
    # print(f'The current vote is {to_str}')

    if not votes:
        new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
        new_vote.save_vote()
    
        # print('you have already votted')

    for vote in votes:
        if f'{vote}' == to_str:
            # print('votting can only be done once')
            break
        else:   
            new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
            new_vote.save_vote()
            # print('You have successfully votted')
            break

    return redirect(url_for('.view_pitch', id=id))


