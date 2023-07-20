from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session
from keys import APP_SECRET_KEY
from auth import CASClient
from os import environ

import database as db

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

# Use this when testing locally
app.secret_key = APP_SECRET_KEY

# Use this when deploying to Heroku
# app.secret_key = environ.get('APP_SECRET_KEY')

_cas = CASClient()

#-----------------------------------------------------------------------

# def not_logged_in():
    # return not _cas.is_logged_in()
    # return not _cas.is_logged_in() or not db.user_exists(_cas.authenticate().rstrip())

@app.route('/login', methods=['GET'])
def login():
    netid = _cas.authenticate()
    netid = netid.rstrip()
    # if not db.user_exists(netid):
    #     db.insert_user(netid)
    return redirect(url_for('practice', lesson_num=1.1))

@app.route('/logout', methods=['GET'])
def logout():
    _cas.logout()

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    html = render_template('landing.html')
    response = make_response(html)
    return response


@app.route('/keyboard', methods=['GET'])
def keyboard():
    netid = _cas.authenticate()
    html = render_template('keyboard.html', netid=netid)
    response = make_response(html)
    return response

@app.route('/lessons', methods=['GET'])
def lessons():
    netid = _cas.authenticate()
    lessons = db.get_lessons()
    html = render_template('lessons.html', lessons=lessons, netid=netid)
    response = make_response(html)
    return response

@app.route('/lessons/<lesson_num>', methods=['GET'])
def practice(lesson_num):
    netid = _cas.authenticate()
    lesson = int(lesson_num.split(".")[0])
    sublesson = int(lesson_num.split(".")[1])
    prev, next = None, None
    if lesson_num == "1.1":
        next = "/lessons/1.2"
    elif lesson_num == "7.2":
        prev = "/lessons/7.1"
    else:
        if sublesson == 2:
            prev = "/lessons/" + str(lesson) + "." + "1"
            next = "/lessons/" + str(lesson+1) + "." + "1"
        else:
            prev = "/lessons/" + str(lesson-1) + "." + "2"
            next = "/lessons/" + str(lesson) + "." + "2"
    text = db.get_text(lesson, sublesson)
    convo = db.get_conversation(lesson, sublesson)
    num_characters = len(''.join(convo.replace('?', '').replace('.', '').replace(',', '').split()))
    html = render_template('practice.html', lesson_num=lesson_num, text=text, prev=prev, next=next, num_characters=num_characters, netid=netid)
    response = make_response(html)
    return response
