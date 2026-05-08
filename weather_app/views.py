from django.shortcuts import render
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))
# Create your views here.
def myrequest(request):
    city = request.GET.get("city", "").strip()
    state = request.GET.get("state", "").strip()
    country = request.GET.get("country", "").strip()

    # --- IF/ELSE LOGIC FOR COUNTRY NAMES ---
    # The API prefers 'NG' over 'Nigeria'. 
    # If a user types 'Nigeria', we can either force it to NG or 
    # just ignore it to let the API search by City alone (which is safer).
    
    if len(country) > 2:
        # If the country is long (e.g., "Nigeria"), it's safer to just search by City
        # or you could map it: if country.lower() == "nigeria": country = "NG"
        query = city 
    else:
        # If it's a 2-letter code or empty, include it in the search
        query_parts = [city, state, country]
        query = ",".join([part for part in query_parts if part])

    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    # Final check for valid API response
    if data.get("cod") == 200:
        return render(request, "details.html", {"data": data})
    else:
        return render(request, "input.html", {"error": "Location not found. Try 'Ibadan, NG'"})
def main(request):
    return render(request, "input.html")
