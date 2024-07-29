import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.models.website import Website
from app.services.crunchbase import generate_summary
import time

# List of websites to analyze
websites = [
    "https://www.shapesxr.com", "https://newhomesmate.com", "https://foodready.ai",
    # ... (rest of the websites)
]

def analyze_website(url, index, total):
    try:
        print(f"[{index+1}/{total}] Visiting {url}")
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "No title found"
        
        # Extract more content
        paragraphs = soup.find_all('p')
        content = ' '.join([p.text for p in paragraphs[:10]])  # Limit to first 10 paragraphs
        
        print(f"[{index+1}/{total}] Finished visiting {url}")
        return url, title, content
    except Exception as e:
        print(f"[{index+1}/{total}] Error visiting {url}: {str(e)}")
        return url, "Error", str(e)

def analyze_all_websites():
    start_time = time.time()
    print(f"Starting analysis of {len(websites)} websites...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(analyze_website, url, i, len(websites)): (i, url) for i, url in enumerate(websites)}
        for future in as_completed(future_to_url):
            index, url = future_to_url[future]
            url, title, content = future.result()
            ai_summary = generate_summary(content, url, index, len(websites))
            Website.create_or_update(url, title, content, ai_summary)
    
    end_time = time.time()
    print(f"Analysis completed in {end_time - start_time:.2f} seconds.")

def get_analyzed_websites():
    return Website.get_all()