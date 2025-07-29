from fastapi import FastAPI
from bs4 import BeautifulSoup
import cloudscraper

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

    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get(url, params=params)
        
        # Debugging if response is empty
        if res.status_code != 200:
            return {"success": False, "error": f"Bad status: {res.status_code}", "raw": res.text}

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        results = []
        for v in soup.find_all("div", class_="result-wrapper"):
            villa_name_elem = v.find("h3")
            price_elem = v.find("span", class_="price")
            if villa_name_elem and price_elem:
                results.append({
                    "name": villa_name_elem.get_text(strip=True),
                    "price": price_elem.get_text(strip=True)
                })

        return {"success": True, "results": results}

    except Exception as e:
        return {"success": False, "error": str(e)}
