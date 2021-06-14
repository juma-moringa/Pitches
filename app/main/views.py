from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . forms import PitchForm, CommentForm, CategoryForm
from .import main
from .. import db
from ..models import User, Pitch, Comments,Category, Votes,Upvote,Downvote

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
@main.route('/comment/<int:id>',methods= ['POST','GET'])
@login_required
def viewPitch(id):
    onepitch = Pitch.getPitchId(id)
    comments = Comments.get_comments(id)

    if request.args.get("like"):
        onepitch.likes = onepitch.likes + 1

        db.session.add(onepitch)
        db.session.commit()

        return redirect("/comment/{pitch_id}".format(pitch_id=category.id))

    elif request.args.get("dislike"):
        onepitch.dislikes = onepitch.dislikes + 1

        db.session.add(onepitch)
        db.session.commit()

        return redirect("/comment/{pitch_id}".format(pitch_id=category.id))

    commentForm = CommentForm()
    if commentForm.validate_on_submit():
        opinion = commentForm.opinion.data

        newComment = Comments(opinion = opinion,user = current_user,pitches_id= id)

        newComment.save_comment()

    return render_template('comment.html',commentForm = commentForm,comments = comments,pitch = onepitch)


@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    pitch = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(username = current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))    


