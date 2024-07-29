from flask import Blueprint, render_template
from app.services.website_analyzer import analyze_all_websites, get_analyzed_websites

bp = Blueprint('website_analyzer', __name__)

@bp.route('/analyze')
def analyze():
    analyze_all_websites()
    websites_data = get_analyzed_websites()
    return render_template('index.html', websites=websites_data)