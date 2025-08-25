import requests
import pycountry
import json
import os
import time

def fetch_radware_threat_data():
    def get_country_name(code):
        if not code or not code.strip():
            return None
        try:
            country = pycountry.countries.get(alpha_2=code.strip().upper())
            return country.name if country else None
        except Exception as e:
            # print(f"Country code error for '{code}': {e}")
            return None

    url = 'https://ltm-prod-api.radware.com/map/attacks?limit=600'

    headers = {
        'Host': 'ltm-prod-api.radware.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://livethreatmap.radware.com',
        'Referer': 'https://livethreatmap.radware.com/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'TE': 'trailers'
    }

    while True:
        try:
            # First debug the API response
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            

            # Debug the parsed JSON structure
            attacks_data = response.json()
            
            threat_data_list = []

            # The response is a list of lists, each containing attack dictionaries
            for attack_group in attacks_data:
                if not isinstance(attack_group, list): # Skip non-list items
                    continue
                    
                for attack in attack_group:
                    if not isinstance(attack, dict):  # Skipping non-dict entry in group
                        continue

                    try:
                        attack_type = attack.get('type')
                        source_country_code = attack.get('sourceCountry', '').strip() or None
                        destination_country_code = attack.get('destinationCountry', '').strip() or None
                        weight = attack.get('weight')
                        attack_time = attack.get('attackTime')

                        threat_data = {
                            "Attack Count": None,
                            "Attack Name": attack_type,
                            "Attack Type": attack_type,
                            "Destination Country Code": destination_country_code,
                            "Destination Country Name": get_country_name(destination_country_code),
                            "Destination Latitude": None,
                            "Destination Longitude": None,
                            "Destination Severity": weight,
                            "Source Country Code": source_country_code,
                            "Source Country Name": get_country_name(source_country_code),
                            "Source Latitude": None,
                            "Source Longitude": None,
                            "Source Severity": None,
                            "Timestamp": attack_time
                        }
                        threat_data_list.append(threat_data)
                    except Exception as e:
                        print(f"Error processing attack: {e}")
                        continue

            # Final debug output
            # print(f"\nTotal processed records: {len(threat_data_list)}")
            # print("Sample output (first record):")
            # if threat_data_list:
            #     print(json.dumps(threat_data_list[0], indent=2))
            # else:
            #     print("No records processed")

            yield threat_data_list
            time.sleep(60)

        except requests.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err}")
            print(f"Response content: {response.text[:500]}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Run directly if needed
if __name__ == "__main__":
    stream = fetch_radware_threat_data()
    for chunk in stream:
        for entry in chunk:
            print(entry)