from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

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

    # Headers include Cloudflare bypass
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.sopranovillas.com/",
        "x-api-secret": "supersecretkey123"  # <-- Cloudflare bypass header
    }

    try:
        res = requests.get(url, params=params, headers=headers)
        res.raise_for_status()

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        villas = []
        for villa_div in soup.find_all("div", class_="result-wrapper"):
            name = villa_div.get("data-property-name", "").strip()
            price = villa_div.get("data-price", "").strip()

            # Get the villa link
            link_tag = villa_div.find("a", href=True)
            link = link_tag["href"] if link_tag else ""
            link = link.replace("\\\"", "").replace("\"", "")

            guests = villa_div.get("data-guests", "")
            bedrooms = villa_div.get("data-rooms", "")
            bathrooms = villa_div.get("data-bathrooms", "")

            # Optional: filter by villa_name
            if villa_name and villa_name.lower() not in name.lower():
                continue

            villas.append({
                "name": name,
                "price": f"{price} €" if price else None,
                "guests": guests,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "url": link
            })

        return {"success": True, "count": len(villas), "results": villas}

    except Exception as e:
        return {"success": False, "error": str(e)}
