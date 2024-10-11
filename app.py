import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Go High Level API credentials
GHL_API_URL = os.getenv("GHL_API_URL")
GHL_API_TOKEN = os.getenv("GHL_API_TOKEN")

# Zoom OAuth credentials
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_TOKEN_URL = os.getenv("ZOOM_TOKEN_URL")

# Zoom API endpoint
ZOOM_API_URL = os.getenv("ZOOM_API_URL")
# Function to get Zoom OAuth access token
def get_zoom_oauth_token():
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(ZOOM_TOKEN_URL, auth=(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET), data=data)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Error fetching Zoom OAuth token:", response.status_code, response.text)
        return None

# Function to get contacts from Go High Level
def get_ghl_contacts():
    headers = {
        'Authorization': f'Bearer {GHL_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(GHL_API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('contacts')
    else:
        print("Error fetching contacts from GHL:", response.status_code)
        return None

# Function to make a call using Zoom Phone
def make_zoom_call(contact_number, zoom_oauth_token):
    headers = {
        'Authorization': f'Bearer {zoom_oauth_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "to": contact_number,  # recipient's phone number
        "from": "your_zoom_phone_number"  # your Zoom Phone number
    }
    response = requests.post(f"{ZOOM_API_URL}/calls", headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Call initiated successfully.")
    else:
        print("Error making Zoom call:", response.status_code, response.text)

# Main logic to integrate Zoom with GHL
def integrate_zoom_with_ghl():
    contacts = get_ghl_contacts()
    if contacts:
        # Get Zoom OAuth access token
        zoom_oauth_token = get_zoom_oauth_token()
        if not zoom_oauth_token:
            print("Unable to get Zoom OAuth token.")
            return
        
        # Loop through contacts and make calls via Zoom
        for contact in contacts:
            contact_number = contact.get('phone')
            if contact_number:
                make_zoom_call(contact_number, zoom_oauth_token)

# Run the integration
integrate_zoom_with_ghl()
