from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, session

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

@app.route('/practice', methods=['GET'])
def practice():
    html = render_template('practice.html')
    response = make_response(html)
    return response
