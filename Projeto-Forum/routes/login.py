from flask import Blueprint, render_template

login_route = Blueprint('home', __name__)

@login_route.route('/')
def home():
    return render_template('login.html')