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
