import requests

url = "https://api.myscheme.gov.in/search/v6/schemes?lang=en&q=%5B%5D&keyword=farmer&sort=&from=0&size=10"

headers = {
    "x-api-key": "YOUR_KEY",
    "origin": "https://www.myscheme.gov.in",
    "referer": "https://www.myscheme.gov.in/",
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

session = requests.Session()

r = session.get(url, headers=headers)

print(r.status_code)
print(r.text[:500])