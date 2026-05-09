import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_product_media(url):
    """
    Scrapes images and videos from a product URL.
    Returns a list of media URLs.
    """
    media_urls = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for images
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                # Basic filtering for product-like images (usually larger)
                if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    full_url = urljoin(url, src)
                    if full_url not in media_urls:
                        media_urls.append(full_url)
        
        # Look for videos
        for video in soup.find_all('video'):
            src = video.get('src')
            if src:
                full_url = urljoin(url, src)
                if full_url not in media_urls:
                    media_urls.append(full_url)
            
            for source in video.find_all('source'):
                src = source.get('src')
                if src:
                    full_url = urljoin(url, src)
                    if full_url not in media_urls:
                        media_urls.append(full_url)

        # Limit to first 20 media items to avoid overwhelming the generator
        return media_urls[:20]

    except Exception as e:
        print(f"Scraping error for {url}: {e}")
        return []
