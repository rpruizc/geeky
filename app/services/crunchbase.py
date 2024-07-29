import requests
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY")

def get_crunchbase_data(company_url):
    # Extract company name or domain from URL
    company_name = company_url.split('://')[1].split('.')[0]
    
    # Crunchbase API endpoint
    api_url = f"https://api.crunchbase.com/v3.1/organizations/{company_name}"
    
    # Parameters for the API request
    params = {
        "user_key": CRUNCHBASE_API_KEY
    }
    
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        
        if 'data' in data:
            company_info = data['data']
            return {
                "name": company_info.get('properties', {}).get('name', 'N/A'),
                "description": company_info.get('properties', {}).get('description', 'N/A'),
                "founded_on": company_info.get('properties', {}).get('founded_on', 'N/A'),
                "website": company_info.get('properties', {}).get('homepage_url', 'N/A'),
                "location": company_info.get('properties', {}).get('city_name', 'N/A') + ", " + 
                            company_info.get('properties', {}).get('country_code', 'N/A'),
            }
        else:
            return {"error": "Company not found or API error"}
    except Exception as e:
        return {"error": str(e)}

def generate_summary(content, url, index, total):
    try:
        print(f"[{index+1}/{total}] Sending content to OpenAI for analysis: {url}")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes website content."},
                {"role": "user", "content": f"Based on the following content from a website, provide a brief summary (2-3 sentences) about what the company does:\n\n{content}"}
            ],
            model="gpt-3.5-turbo",
        )
        summary = chat_completion.choices[0].message.content.strip()
        print(f"[{index+1}/{total}] Received analysis from OpenAI: {url}")
        return summary
    except Exception as e:
        print(f"[{index+1}/{total}] Error generating summary for {url}: {str(e)}")
        return f"Error generating summary: {str(e)}"