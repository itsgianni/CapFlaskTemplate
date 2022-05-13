# These routes are an example of how to use data, forms and routes to create
# a forum where a posts and comments on those posts can be
# Created, Read, Updated or Deleted (CRUD)

from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Question, Comment
from app.classes.forms import QuestionForm, CommentForm
from flask_login import login_required
import datetime as dt

#--------------------------CREATE---------------------------------
@app.route('/question/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def questionNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = QuestionForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new post form. 
        # Post() is a mongoengine method for creating a new post. 'newPost' is the variable 
        # that stores the object that is the result of the Post() method.  
        newQuestion = Question(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            subject = form.subject.data,
            content = form.content.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modifydate = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newQuestion.save()

        # Once the new post is saved, this sends the user to that post using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a post so we want 
        # to send them to that post. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('question',questionID=newQuestion.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at postform.html to 
    # see how that works.
    return render_template('questionform.html',form=form)

#--------------------------EDIT---------------------------------

@app.route('/question/edit/<questionID>', methods=['GET', 'POST'])
@login_required
def questionEdit(questionID):
    editQuestion = Question.objects.get(id=questionID)
    # if the user that requested to edit this post is not the author then deny them and
    # send them back to the post. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editQuestion.author:
        flash("You can't edit a question you don't own.")
        return redirect(url_for('question',questionID=questionID))
    # get the form object
    form = QuestionForm()
    # If the user has submitted the form then update the post.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editQuestion.update(
            subject = form.subject.data,
            content = form.content.data,
            modifydate = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated post using a redirect.
        return redirect(url_for('question',questionID=questionID))

    # if the form has NOT been submitted then take the data from the editPost object
    # and place it in the form object so it will be displayed to the user on the template.
    form.subject.data = editQuestion.subject
    form.content.data = editQuestion.content

    # Send the user to the post form that is now filled out with the current information
    # from the form.
    return render_template('questionform.html',form=form)

#--------------------------DELETE---------------------------------

@app.route('/question/delete/<questionID>')
# Only run this route if the user is logged in.
@login_required
def questionDelete(questionID):
    # retrieve the post to be deleted using the postID
    deleteQuestion = Question.objects.get(id=questionID)
    # check to see if the user that is making this request is the author of the post.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteQuestion.author:
        # delete the post using the delete() method from Mongoengine
        deleteQuestion.delete()
        # send a message to the user that the post was deleted.
        flash('The Question was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a question you don't own.")
    # Retrieve all of the remaining posts so that they can be listed.
    questions = Question.objects()  
    # Send the user to the list of remaining posts.
    return render_template('questions.html',questions=questions)

#--------------------------view one---------------------------------

@app.route('/question/<questionID>')
# This route will only run if the user is logged in.
@login_required
def question(questionID):
    # retrieve the post using the postID
    thisQuestion = Question.objects.get(id=questionID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to posts meaning that every comment contains a reference to a post. In this case
    # there is a field on the comment collection called 'post' that is a reference the Post
    # document it is related to.  You can use the postID to get the post and then you can use
    # the post object (thisPost in this case) to get all the comments.
    # Send the post object and the comments object to the 'post.html' template.
    return render_template('Question.html',question=thisQuestion)

#--------------------------view all---------------------------------

# This is the route to list all posts
@app.route('/questions')
# This means the user must be logged in to see this page
@login_required
def questionList():
    # This retrieves all of the 'posts' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'posts'.
    questions = Question.objects()
    # This renders (shows to the user) the posts.html template. it also sends the posts object 
    # to the template as a variable named posts.  The template uses a for loop to display
    # each post.
    return render_template('questions.html',questions=questions)

#-------------------Comments-------------------------------
@app.route('/comment/new/<questionID>', methods=['GET', 'POST'])
@login_required
def commentNew(questionID):
    question = Question.objects.get(id=questionID)
    form = CommentForm()
    if form.validate_on_submit():
        newComment = Comment(
            author = current_user.id,
            question = questionID,
            content = form.content.data,
        )
        newComment.save()
        return redirect(url_for('question',questionID=questionID))
    return render_template('commentform.html',form=form,question=question)

@app.route('/comment/edit/<commentID>', methods=['GET', 'POST'])
@login_required
def commentEdit(commentID):
    editComment = Comment.objects.get(id=commentID)
    if current_user != editComment.author:
        flash("You can't edit a comment you didn't write.")
        return redirect(url_for('question',questionID=editComment.question.id))
    question = Question.objects.get(id=editComment.question.id)
    form = CommentForm()
    if form.validate_on_submit():
        editComment.update(
            content = form.content.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('question',questionID=editComment.question.id))

    form.content.data = editComment.content

    return render_template('commentform.html',form=form,question=question)   

@app.route('/comment/delete/<commentID>')
@login_required
def commentDelete(commentID): 
    deleteComment = Comment.objects.get(id=commentID)
    deleteComment.delete()
    flash('The comments was deleted.')
    return redirect(url_for('question',questionID=deleteComment.question.id))

