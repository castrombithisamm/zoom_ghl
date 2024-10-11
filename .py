from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Constants for Zoom API
ZOOM_JWT_TOKEN = 'YOUR_ZOOM_JWT_TOKEN'  # Use your JWT for Zoom API
ZOOM_FROM_NUMBER = 'YOUR_ZOOM_PHONE_NUMBER'  # Your Zoom number

@app.route('/api/initiate_call', methods=['POST'])
def initiate_call():
    try:
        # Extract contact number from the request
        data = request.json
        contact_number = data.get('contact_number')

        # Prepare the call request
        zoom_url = 'https://api.zoom.us/v2/phone/call'
        headers = {
            'Authorization': f'Bearer {ZOOM_JWT_TOKEN}',
            'Content-Type': 'application/json'
        }
        call_data = {
            'to': contact_number,
            'from': ZOOM_FROM_NUMBER
        }

        # Make a request to the Zoom phone API to initiate a call
        response = requests.post(zoom_url, json=call_data, headers=headers)

        if response.status_code == 200:
            return jsonify({"message": "Call initiated successfully."}), 200
        else:
            return jsonify({"error": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)