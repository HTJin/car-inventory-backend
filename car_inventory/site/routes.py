from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='site_template')

@site.route('/')
def home():
    return render_template('index.html')