from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page"

@app.route("/auth/oidc/callback")
def callback():
    return "not yet implemented :("