from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/lessonMaking')
def lessonMaking():
    return render_template('lessonMaking.html')

@app.route('/lessonInvesting')
def lessonInvesting():
    return render_template('lessonInvesting.html')

@app.route('/lessonBudgeting')
def lessonBudgeting():
    return render_template('lessonBudgeting.html')

@app.route('/lessonSaving')
def lessonSaving():
    return render_template('lessonSaving.html')

@app.route('/lessonBorrowing')
def lessonBorrowing():
    return render_template('lessonBorrowing.html')

@app.route('/lessonSpending')
def lessonSpending():
    return render_template('lessonSpending.html')

@app.route('/lessonProtect')
def lessonProtect():
    return render_template('lessonProtect.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')