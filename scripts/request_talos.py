import requests
import json
import time

def fetch_talos_spam_data():
    url = "https://talosintelligence.com/cloud_intel/top_senders_list"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://talosintelligence.com/reputation_center',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            parsed = []

            for entry in data.get("spam", []):
                coords = entry.get("geo_coords", {})
                country = entry.get("country_info", {})

                parsed_entry = {
                    "Attack Count": entry.get("day_magnitude_x10"),
                    "Attack Name": "Spam",
                    "Attack Type": "Spam",
                    "Destination Country Code": None,
                    "Destination Country Name": None,
                    "Destination Latitude": None,
                    "Destination Longitude": None,
                    "Destination Severity": None,
                    "Source Country Code": country.get("code"),
                    "Source Country Name": country.get("name"),
                    "Source Longitude": coords.get("longitude_x10000") / 10000 if coords.get("longitude_x10000") else None,
                    "Source Latitude": coords.get("latitude_x10000") / 10000 if coords.get("latitude_x10000") else None,
                    "Source Severity": entry.get("day_magnitude_x10"),
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                parsed.append(parsed_entry)

            return parsed
        else:
            return {"error": f"Status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Run every 30 seconds
if __name__ == "__main__":
    while True:
        result = fetch_talos_spam_data()
        print(json.dumps(result, indent=2))
        time.sleep(30)
