import os
from flask import Flask

from modules import init
from modules import functions

conf = init.config('web')
con, cur = init.getdb()

redirect_url = conf.get_redirect_url()

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__)

@app.route("/")
def index():
    #TODO there should be someting like templates in flask, so you just return the function with the html file without opening it manually first :D
    with open("Include/index.html", 'r') as p:
        page = p.read()
    return page

@app.route("/init")
def init():
    cur.execute(f"INSERT OR IGNORE INTO user VALUES (4, 'baum', 'https://url.com', 'lol', '88:ia', {False}, {False}, '', '', '')")
    con.commit()
    return 'uwu'

@app.route("/update")
def update():
    cur.execute(f"UPDATE user SET state = 'boom' WHERE id = 4")
    con.commit()
    return 'owo'

@app.route(f"/{redirect_url}")
def callback():
    state = 'boom'
    cloak_id = 0
    email = ''
    cur.execute(f"SELECT id FROM user WHERE state = '{state}'")
    if len(cur.fetchall()) != 1:
        return "400 Bad Request"
    cur.execute(f"SELECT id FROM user WHERE cloak_id = '{cloak_id}'")
    if len(cur.fetchall()) > 0:
        return "403 Forbidden" #TODO maybe add some user information that their keycloak is already linked to another account and maybe some way to contact the admins for fixing it
    cur.execute(f"UPDATE user SET is_verified = {True}, cloak_id = '{cloak_id}', email = '{email}', state = NULL WHERE state = '{state}'")
    con.commit()
    # await functions.syncWhitelist()
    return "not yet implemented :(" #TODO a nice html page with a confirmation