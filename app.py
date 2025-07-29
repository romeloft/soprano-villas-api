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

        # If Cloudflare is blocking, we’ll get a debug response
        debug_info = {
            "debug_url": res.url,
            "status_code": res.status_code,
            "headers": dict(res.headers),
            "raw_response_start": res.text[:500]  # first 500 chars only
        }

        if res.status_code != 200:
            return {"success": False, "error": "Bad status", "debug": debug_info}

        # Try parsing HTML
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for v in soup.find_all("div", class_="result-wrapper"):
            villa_name_elem = v.find("h3")
            price_elem = v.find("span", class_="price")
            if villa_name_elem and price_elem:
                results.append({
                    "name": villa_name_elem.get_text(strip=True),
                    "price": price_elem.get_text(strip=True)
                })

        if not results:
            return {"success": False, "error": "No villas parsed", "debug": debug_info}

        return {"success": True, "results": results}

    except Exception as e:
        return {"success": False, "error": str(e)}
