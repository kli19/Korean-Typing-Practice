from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session

import database as db

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/keyboard', methods=['GET'])
def keyboard():
    html = render_template('keyboard.html')
    response = make_response(html)
    return response

@app.route('/lessons', methods=['GET'])
def lessons():
    print("we are here")
    lessons = db.get_lessons()
    print("success")
    html = render_template('lessons.html', lessons=lessons)
    response = make_response(html)
    return response

@app.route('/practice/<lesson_num>', methods=['GET'])
def practice(lesson_num):
    lesson = int(lesson_num.split(".")[0])
    sublesson = int(lesson_num.split(".")[1])
    text = db.get_text(lesson, sublesson)
    print(text)
    html = render_template('practice.html', text=text)
    response = make_response(html)
    return response
