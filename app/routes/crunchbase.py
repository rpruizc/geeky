from flask import Blueprint, render_template, request, flash
from app.services.crunchbase import get_crunchbase_data
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('crunchbase', __name__)

@bp.route('/crunchbase', methods=['GET', 'POST'])
def crunchbase():
    if request.method == 'POST':
        company_url = request.form['company_url']
        logger.info(f"Received request for Crunchbase data: {company_url}")
        company_data = get_crunchbase_data(company_url)
        if 'error' in company_data:
            flash(company_data['error'], 'error')
            logger.error(f"Error in Crunchbase data retrieval: {company_data['error']}")
        return render_template('crunchbase.html', company_data=company_data)
    return render_template('crunchbase.html')