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

    try:
        res = requests.get(url, params=params)
        data = res.json() if res.headers.get('Content-Type') == 'application/json' else res.text

        if isinstance(data, dict) and "data" in data:
            html = data["data"]
        else:
            html = data

        soup = BeautifulSoup(html, "html.parser")

       results = []
for villa in soup.find_all("div", class_="result-wrapper"):
    name = villa.get("data-property-name")
    price = villa.get("data-price")
    link = villa.find("a", href=True)["href"]
    if villa_name is None or villa_name.lower() in name.lower():
        results.append({
            "name": name,
            "price": price,
            "url": link
        })

return {
    "success": True,
    "count": len(results),  # <== show number of results
    "results": results
}

