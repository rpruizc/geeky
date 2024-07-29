from app import create_app
from app.models.website import init_db
from app.services.website_analyzer import analyze_all_websites
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized.")
        
        logger.info("Starting website analysis...")
        analyze_all_websites()
        logger.info("Website analysis completed.")
    
    logger.info("Starting Flask development server...")
    app.run(debug=True)