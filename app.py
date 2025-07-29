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
        res = requests.get(url, params=params).json()
        html = res["data"]
        soup = BeautifulSoup(html, "html.parser")

        # Find villa(s)
        result = None
        for v in soup.find_all("div", class_="result-wrapper"):
            name = v.get("data-property-name")
            price = v.get("data-price")
            link = v.find("a")["href"]

            if villa_name:
                if villa_name.lower() in name.lower():
                    result = {"name": name, "price": price, "url": link}
                    break
            else:
                if not result:
                    result = {"name": name, "price": price, "url": link}

        if not result:
            return {"success": False, "message": "No villa found"}

        return {"success": True, "villa": result}

    except Exception as e:
        return {"success": False, "error": str(e)}
