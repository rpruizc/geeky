from flask import Blueprint, render_template, jsonify
from app.models.website import Website

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/debug/websites')
def debug_websites():
    websites = Website.get_all()
    return jsonify([dict(website) for website in websites])