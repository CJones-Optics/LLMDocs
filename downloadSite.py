import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def download_page(url, output_dir):
    """Downloads the content of a URL and saves it to a local file."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        parsed_url = urlparse(url)
        path = parsed_url.path.strip('/')
        if not path or path.endswith('/'):
            filename = "index.html"
        else:
            filename = path.replace('/', '_')
            if not filename.endswith(".html"):
                filename += ".html"

        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Downloaded: {url} -> {filepath}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def find_html_links(base_url, html_content):
    """Finds all HTML links within a given HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute_url = urljoin(base_url, href)
        if absolute_url.startswith(base_url) and absolute_url.endswith(".html"):
            links.add(absolute_url)
        elif absolute_url.startswith(base_url) and not urlparse(absolute_url).path.split('/')[-1].count('.'):
            # Handle cases where the link might be to a directory with an implicit index.html
            if not absolute_url.endswith('/'):
                links.add(absolute_url + "/")
            else:
                links.add(absolute_url)
    return links

def crawl_readthedocs(base_url, output_dir):
    """Crawls a Read the Docs webpage and downloads all HTML files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    visited_urls = set()
    queue = [base_url]

    while queue:
        current_url = queue.pop(0)

        if current_url in visited_urls:
            continue
        visited_urls.add(current_url)

        print(f"Processing: {current_url}")
        html_content = download_page(current_url, output_dir)

        if html_content:
            new_links = find_html_links(base_url, html_content)
            for link in new_links:
                if link not in visited_urls and link not in queue:
                    queue.append(link)

if __name__ == "__main__":
    readthedocs_url = input("Enter the base URL of your Read the Docs webpage (e.g., https://your-project.readthedocs.io/en/latest/): ").strip()
    output_directory = input("Enter the local directory to save the documentation (e.g., ./readthedocs_docs): ").strip()

    if not readthedocs_url.endswith('/'):
        readthedocs_url += '/'

    crawl_readthedocs(readthedocs_url, output_directory)
    print("Crawling and downloading complete.")