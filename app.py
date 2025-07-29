import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Sopranovillas Price API is running!"}

@app.get("/get_price")
def get_price(region: str, checkin: str, checkout: str, adults: int, villa_name: str = None):
    url = "https://www.sopranovillas.com/wp-admin/admin-ajax.php"
    params = {
        "action": "so_get_villa_results",
        "region": region,
        "theDates": "",
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.sopranovillas.com/"
    }

    try:
        res = requests.get(url, params=params, headers=headers)
        res.raise_for_status()

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        # Just an example: extract villa results
        results = []
        for v in soup.find_all("div", class_="result-wrapper"):
            results.append(v.get_text(strip=True))

        return {"success": True, "results": results}

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/debug_ip")
def debug_ip():
    import requests
    ip = requests.get("https://api.ipify.org").text
    return {"server_ip": ip}

