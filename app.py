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
        raw_text = res.text  # Debug: see raw response

        # Return raw response for debugging
        return {
            "success": False,
            "debug_url": res.url,
            "raw_response": raw_text[:500]  # first 500 chars only
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
