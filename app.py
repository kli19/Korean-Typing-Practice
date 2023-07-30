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
    admins = db.get_admins()
    isadmin = netid in admins
    lessons = db.get_lessons()
    html = render_template('lessons.html', lessons=lessons, netid=netid, isadmin=isadmin)
    response = make_response(html)
    return response

@app.route('/lessons/<lesson_num>', methods=['GET'])
def practice(lesson_num):
    netid = _cas.authenticate()
    lesson = int(lesson_num.split(".")[0])
    sublesson = int(lesson_num.split(".")[1])
    prev, next = None, None
    existing_lessons = db.get_existing_lesson_nums()
    existing_lessons.sort()
    index = existing_lessons.index(lesson)
    if index == 0 and sublesson == 1:
        next = "/lessons/" + str(lesson) + ".2"
    elif index == len(existing_lessons)-1 and sublesson == 2:
        prev = "/lessons/" + str(lesson) + ".1"
    else:
        if sublesson == 2:
            prev = "/lessons/" + str(lesson) + "." + "1"
            next = "/lessons/" + str(existing_lessons[index+1]) + "." + "1"
        else:
            prev = "/lessons/" + str(existing_lessons[index-1]) + "." + "2"
            next = "/lessons/" + str(lesson) + "." + "2"
    text = db.get_lesson_text(lesson, sublesson)
    convo = db.get_conversation(lesson, sublesson)
    num_characters = len(''.join(convo.replace('?', '').replace('.', '').replace(',', '').split()))
    html = render_template('practice.html', lesson_num=lesson_num, text=text, prev=prev, next=next, num_characters=num_characters, netid=netid)
    response = make_response(html)
    return response

@app.route('/editlessons', methods=['GET'])
def editlessons():
    netid = _cas.authenticate()
    admins = db.get_admins()
    isadmin = netid in admins
    if not isadmin:
        return redirect(url_for('index'))
    lessons = db.get_lessons()
    html = render_template('editlessons.html', lessons=lessons, netid=netid, isadmin=isadmin)
    response = make_response(html)
    return response


@app.route('/makelesson', methods=['GET'])
def makelesson():
    netid = _cas.authenticate()
    admins = db.get_admins()
    isadmin = netid in admins
    existing_lessons = db.get_existing_lesson_nums()
    if not isadmin:
        return redirect(url_for('index'))
    html = render_template('makelesson.html', netid=netid, isadmin=isadmin, existing_lessons=existing_lessons)
    response = make_response(html)
    return response

@app.route('/addlesson', methods=['GET','POST'])
def addlesson():
    netid = _cas.authenticate()
    admins = db.get_admins()
    isadmin = netid in admins
    if not isadmin:
        return redirect(url_for('index'))
    dic = request.form

    lesson_info = {"lesson": int(dic["lesson"]),
                    "title_kor": dic["lesson_title_kor"],
                    "title_en": dic["lesson_title_en"],
                    "sublessons": [{"sublesson": 1,
                                    "title_kor": dic["sublesson1_title_kor"],
                                    "title_en": dic["sublesson1_title_en"],
                                    "text": dic["sublesson1_text"].strip()},
                                    {"sublesson": 2,
                                    "title_kor": dic["sublesson2_title_kor"],
                                    "title_en": dic["sublesson2_title_en"],
                                    "text": dic["sublesson2_text"].strip()}]}
    db.insert_lesson(lesson_info)
    return redirect(url_for('lessons'))

@app.route('/removelesson', methods=['GET','POST'])
def removelesson():
    netid = _cas.authenticate()
    admins = db.get_admins()
    isadmin = netid in admins
    if not isadmin:
        return redirect(url_for('index'))
    lesson = int(request.args.get("lesson"))
    db.delete_lesson(lesson)
    return redirect(url_for('lessons'))

@app.route('/editlesson', methods=['GET', 'POST'])
def editlesson():
    netid = _cas.authenticate()
    admins = db.get_admins()
    isadmin = netid in admins
    if not isadmin:
        return redirect(url_for('index'))
    lesson = int(request.args.get("lesson"))
    lesson_info = db.get_lesson(lesson)
    html = render_template('editlesson.html', lesson_info=lesson_info, netid=netid, isadmin=isadmin)
    response = make_response(html)
    return response

@app.route('/updatelesson', methods=['GET', 'POST'])
def updatelesson():
    netid = _cas.authenticate()
    admins = db.get_admins()
    isadmin = netid in admins
    if not isadmin:
        return redirect(url_for('index'))
    dic = request.form

    lesson_info = {"lesson": int(dic["lesson"]),
                    "title_kor": dic["lesson_title_kor"],
                    "title_en": dic["lesson_title_en"],
                    "sublessons": [{"sublesson": 1,
                                    "title_kor": dic["sublesson1_title_kor"],
                                    "title_en": dic["sublesson1_title_en"],
                                    "text": dic["sublesson1_text"].strip()},
                                    {"sublesson": 2,
                                    "title_kor": dic["sublesson2_title_kor"],
                                    "title_en": dic["sublesson2_title_en"],
                                    "text": dic["sublesson2_text"].strip()}]}
    db.update_lesson(lesson_info)
    return redirect(url_for('lessons'))
