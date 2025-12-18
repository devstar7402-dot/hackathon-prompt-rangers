import requests
import json
import os
from dotenv import load_dotenv

def geocode_address(address, api_key):
    # Base URL for the Geocoding API
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # Construct the full request URL
    params = {
        'address': address,
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()

    print(f"API Response: {data}")  # Print the full API response for debugging
    
    # Check if the API returned a result
    if data['status'] == 'OK' and data['results']:
        location = data['results'][0]['geometry']['location']
        # Return the latitude and longitude
        return location['lat'], location['lng']
    else:
        return None, None

# Load environment variables from .env file
load_dotenv()

# Example usage for your agent's input
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
print(f"API Key: {api_key}")  # Print the API key being used
LAT, LONG = geocode_address("300 S Brevard St, Charlotte, NC 28202", api_key)
