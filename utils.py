import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_internal_link(link, base_netloc):
    try:
        parsed = urlparse(link)
        return parsed.netloc == '' or parsed.netloc == base_netloc
    except:
        return False

def fetch_links(base_url, depth=1):
    visited = set()
    to_visit = [base_url]
    all_texts = []

    base_netloc = urlparse(base_url).netloc

    while to_visit and depth > 0:
        next_to_visit = []
        for url in to_visit:
            if url in visited:
                continue
            visited.add(url)

            try:
                resp = requests.get(url, timeout=5)
                if not resp.ok:
                    continue

                soup = BeautifulSoup(resp.content, 'html.parser')
                body = soup.find('body')
                if body:
                    text = body.get_text(separator='\n', strip=True)
                    if len(text) > 200:
                        all_texts.append(text)

                for tag in soup.find_all('a', href=True):
                    full_url = urljoin(url, tag['href'])
                    if is_internal_link(full_url, base_netloc) and full_url not in visited:
                        next_to_visit.append(full_url)

            except Exception as e:
                continue

        to_visit = next_to_visit
        depth -= 1

    return all_texts
