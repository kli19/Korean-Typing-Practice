from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session

import database as db

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('keyboard'))

@app.route('/keyboard', methods=['GET'])
def keyboard():
    html = render_template('keyboard.html')
    response = make_response(html)
    return response

@app.route('/lessons', methods=['GET'])
def lessons():
    lessons = db.get_lessons()
    html = render_template('lessons.html', lessons=lessons)
    response = make_response(html)
    return response

@app.route('/practice/<lesson_num>', methods=['GET'])
def practice(lesson_num):
    lesson = int(lesson_num.split(".")[0])
    sublesson = int(lesson_num.split(".")[1])
    prev, next = None, None
    if lesson_num == "1.1":
        next = "/practice/1.2" 
    elif lesson_num == "7.2":
        prev = "/practice/7.1"
    else:
        if sublesson == 2:
            prev = "/practice/" + str(lesson) + "." + "1"
            next = "/practice/" + str(lesson+1) + "." + "1"
        else:
            prev = "/practice/" + str(lesson-1) + "." + "2"
            next = "/practice/" + str(lesson) + "." + "2"
    text = db.get_text(lesson, sublesson)
    html = render_template('practice.html', lesson_num=lesson_num, text=text, prev=prev, next=next)
    response = make_response(html)
    return response
