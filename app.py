from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

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

        # Log the full URL and response to Railway logs
        logging.info(f"Request URL: {res.url}")
        logging.info(f"Raw Response (first 1000 chars): {res.text[:1000]}")

        return {
            "success": False,
            "debug_url": res.url,
            "raw_response": res.text[:500]  # return first 500 chars in the browser
        }

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"success": False, "error": str(e)}
