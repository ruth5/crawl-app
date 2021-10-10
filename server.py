"""Server for crawl app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import os
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'saddfkjaksdjfka;lsdfzxcjewmr.,9324'
app.jinja_env.undefined = StrictUndefined

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

@app.route('/')
def show_homepage():
    """View homepage"""
    
    return render_template('index.html', GOOGLE_API_KEY=GOOGLE_API_KEY)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)