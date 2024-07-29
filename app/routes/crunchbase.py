from flask import Blueprint, render_template, request
from app.services.crunchbase import get_crunchbase_data

bp = Blueprint('crunchbase', __name__)

@bp.route('/crunchbase', methods=['GET', 'POST'])
def crunchbase():
    if request.method == 'POST':
        company_url = request.form['company_url']
        company_data = get_crunchbase_data(company_url)
        return render_template('crunchbase.html', company_data=company_data)
    return render_template('crunchbase.html')