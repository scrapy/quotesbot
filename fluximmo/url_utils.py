from urllib.parse import urlparse

def clean_url(url, should_clean_query_params=True):
    if url is None or len(url) == 0:
        return url
    if should_clean_query_params and "?" in url:
        url = url.split("?")[0]
    if url[-1] == "/":
        url = url[:-1]
    return url

def extract_website(url):
    website = urlparse(url).netloc
    if website.startswith("www."):
        website = website[4:]
    if "seloger.com" in url:
        return "seloger.com"
    return website