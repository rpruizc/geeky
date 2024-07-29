import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.models.website import Website
import time
import logging
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

# OpenAI API setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# List of websites to analyze
websites = [
    "https://www.shapesxr.com", "https://newhomesmate.com", "https://foodready.ai",
    # ... (rest of the websites)
]

def analyze_website(url, index, total):
    try:
        logger.info(f"[{index+1}/{total}] Visiting {url}")
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "No title found"
        
        # Extract more content
        paragraphs = soup.find_all('p')
        content = ' '.join([p.text for p in paragraphs[:10]])  # Limit to first 10 paragraphs
        
        logger.info(f"[{index+1}/{total}] Finished visiting {url}")
        return url, title, content
    except Exception as e:
        logger.error(f"[{index+1}/{total}] Error visiting {url}: {str(e)}")
        return url, "Error", str(e)

def generate_summary(content, url, index, total):
    try:
        logger.info(f"[{index+1}/{total}] Sending content to OpenAI for analysis: {url}")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes website content."},
                {"role": "user", "content": f"Based on the following content from a website, provide a brief summary (2-3 sentences) about what the company does:\n\n{content}"}
            ],
            model="gpt-3.5-turbo",
        )
        summary = chat_completion.choices[0].message.content.strip()
        logger.info(f"[{index+1}/{total}] Received analysis from OpenAI: {url}")
        return summary
    except Exception as e:
        logger.error(f"[{index+1}/{total}] Error generating summary for {url}: {str(e)}")
        return f"Error generating summary: {str(e)}"

def analyze_all_websites():
    start_time = time.time()
    logger.info(f"Starting analysis of {len(websites)} websites...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(analyze_website, url, i, len(websites)): (i, url) for i, url in enumerate(websites)}
        for future in as_completed(future_to_url):
            index, url = future_to_url[future]
            url, title, content = future.result()
            ai_summary = generate_summary(content, url, index, len(websites))
            Website.create_or_update(url, title, content, ai_summary)
    
    end_time = time.time()
    logger.info(f"Analysis completed in {end_time - start_time:.2f} seconds.")

def get_analyzed_websites():
    return Website.get_all()