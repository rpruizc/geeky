import requests
import os
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY")
CRUNCHBASE_API_URL = "https://api.crunchbase.com/api/v4/entities/organizations"

def extract_company_identifier(input_string):
    # If it's a URL, extract the domain
    if input_string.startswith(('http://', 'https://')):
        parsed_url = urlparse(input_string)
        return parsed_url.netloc.split('.')[-2]
    # Otherwise, use the input as is (assuming it's already a company identifier)
    return input_string.lower().replace(' ', '-')

def get_crunchbase_data(company_input):
    logger.info(f"Fetching Crunchbase data for: {company_input}")
    company_identifier = extract_company_identifier(company_input)
    
    # API endpoint
    api_url = f"{CRUNCHBASE_API_URL}/{company_identifier}"
    
    # Parameters for the API request
    params = {
        "card_ids": "founders,raised_funding_rounds",
        "field_ids": "categories,short_description,rank_org_company,founded_on,website,facebook,created_at",
        "user_key": CRUNCHBASE_API_KEY
    }
    
    try:
        logger.info(f"Sending request to Crunchbase API for company: {company_identifier}")
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        if 'properties' in data:
            properties = data['properties']
            cards = data.get('cards', {})
            
            founders = [f"{founder['properties']['first_name']} {founder['properties']['last_name']}" 
                        for founder in cards.get('founders', {}).get('items', [])]
            
            funding_rounds = [
                {
                    "type": round['properties'].get('funding_type', 'N/A'),
                    "money_raised": round['properties'].get('money_raised', 'N/A'),
                    "announced_on": round['properties'].get('announced_on', 'N/A')
                }
                for round in cards.get('raised_funding_rounds', {}).get('items', [])
            ]
            
            company_info = {
                "name": properties.get('name', 'N/A'),
                "website": properties.get('website', {}).get('value', 'N/A'),
                "facebook": properties.get('facebook', {}).get('value', 'N/A'),
                "categories": [cat['value'] for cat in properties.get('categories', [])],
                "short_description": properties.get('short_description', 'N/A'),
                "founded_on": properties.get('founded_on', 'N/A'),
                "rank_org_company": properties.get('rank_org_company', 'N/A'),
                "created_at": properties.get('created_at', 'N/A'),
                "founders": founders,
                "funding_rounds": funding_rounds
            }
            
            logger.info(f"Successfully retrieved data for company: {company_identifier}")
            return company_info
        else:
            logger.warning(f"No data found for company: {company_identifier}")
            return {"error": f"No data found for company: {company_identifier}"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Crunchbase API: {str(e)}")
        return {"error": f"Error fetching data from Crunchbase API: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error in get_crunchbase_data: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}