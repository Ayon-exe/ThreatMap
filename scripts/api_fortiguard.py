import requests
import time
import json
import pycountry
from datetime import datetime

# Country code ↔ name helpers
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code.upper()).name
    except:
        return None

def get_country_code(name):
    try:
        return pycountry.countries.search_fuzzy(name)[0].alpha_2
    except:
        return None

def api_fortiguard():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Referer": "https://fortiguard.fortinet.com/threat-map",
    }

    url = "https://fortiguard.fortinet.com/api/threatmap/live/outbreak"
    params = {
        "outbreak_id": 0
    }

    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                time.sleep(5)
                continue

            data = response.json()
            print(data)

            parsed_data = []

            for attack in data.get("attacks", []):
                dst_cc = attack.get("dst_country", None)
                src_cc = attack.get("src_country", None)

                attack_entry = {
                    'Attack Count': attack.get("count", None),
                    'Attack Name': attack.get("name", None),
                    'Attack Type': attack.get("type", None),
                    'Destination Country Code': dst_cc,
                    'Destination Country Name': get_country_name(dst_cc) if dst_cc else None,
                    'Destination Latitude': attack.get("dst_lat", None),
                    'Destination Longitude': attack.get("dst_lon", None),
                    'Destination Severity': attack.get("dst_sev", None),
                    'Source Country Code': src_cc,
                    'Source Country Name': get_country_name(src_cc) if src_cc else None,
                    'Source Latitude': attack.get("src_lat", None),
                    'Source Longitude': attack.get("src_lon", None),
                    'Source Severity': attack.get("src_sev", None),
                    'Timestamp': None  # live stream, no timestamp
                }

                parsed_data.append(attack_entry)

            yield parsed_data
            time.sleep(5)  # stream every 5 seconds

        except Exception as e:
            print("Exception:", e)
            time.sleep(10)

if __name__ == "__main__":
    stream = api_fortiguard()
    for chunk in stream:
        for entry in chunk:
            print(entry)
