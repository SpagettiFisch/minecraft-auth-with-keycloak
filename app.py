import os
from flask import Flask

from modules import init

conf = init.config('web')

redirect_url = conf.get_redirect_url()

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__)

@app.route("/")
def index():
    #TODO there should be someting like emplates in flask, so you just return the function with the html file without opening it manually first :D
    with open("Include/index.html", 'r') as p:
        page = p.read()
    return page

@app.route(f"/{redirect_url}")
def callback():
    return "not yet implemented :("