import requests
import json
import re
import time
import logging
import pycountry

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_country_code(name):
    if not name or not name.strip():
        return None
    if name.lower() == "turkey":
        name = "Türkiye"
    try:
        country = pycountry.countries.search_fuzzy(name)[0]
        return country.alpha_2
    except LookupError:
        logging.warning(f"Could not find country code for '{name}'")
        return None

def fetch_fraudguard_data():
    url = 'https://api.fraudguard.io/landing-page-map'
    headers = {
        'Host': 'api.fraudguard.io',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        'TE': 'trailers'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("API request successful, status code: %s", response.status_code)
        match = re.search(r'const threatData = (\[.*?\]);', response.text, re.DOTALL)
        if not match:
            logging.error("Regex failed to find threatData in response: %s", response.text[:200])
            raise ValueError("Could not find threatData in HTML response")
        json_str = match.group(1)
        attacks_data = json.loads(json_str)
        if not attacks_data:
            logging.warning("Fetched data is empty")
            return []
        return attacks_data
    except requests.HTTPError as http_err:
        logging.error("HTTP error occurred: %s", http_err)
        raise
    except json.JSONDecodeError as json_err:
        logging.error("JSON decode error: %s, Response content: %s", json_err, response.text[:500])
        raise
    except Exception as e:
        logging.error("An error occurred in fetch_fraudguard_data: %s", e)
        raise

def stream_fraudguard_data(interval=10):
    previous_data = None
    backoff_time = interval
    max_backoff = 600
    while True:
        try:
            data = fetch_fraudguard_data()
            backoff_time = interval

            if data:
                sample_countries = [attack.get('country', '') for attack in data[:5]]
                logging.debug("Sample countries in raw data: %s", sample_countries)
            else:
                logging.info("No raw data returned from fetch_fraudguard_data")
                yield []
                continue

            transformed_data = []
            for attack in data:
                country_name = attack.get('country', '').strip() or None
                country_code = get_country_code(country_name) if country_name else None
                threat_data = {
                    "Attack Count": None,
                    "Attack Name": attack.get('threat'),
                    "Attack Type": attack.get('threat'),
                    "Destination Country Code": country_code,
                    "Destination Country Name": country_name,
                    "Destination Latitude": attack.get('latitude'),
                    "Destination Longitude": attack.get('longitude'),
                    "Destination Severity": attack.get('risk'),
                    "Source Country Code": None,
                    "Source Country Name": None,
                    "Source Latitude": None,
                    "Source Longitude": None,
                    "Source Severity": None,
                    "Timestamp": None
                }
                transformed_data.append(threat_data)

            if transformed_data:
                sample_mappings = [
                    f"{entry['Destination Country Name']} -> {entry['Destination Country Code']}"
                    for entry in transformed_data[:5]
                ]
                logging.debug("Sample country code mappings: %s", sample_mappings)

            if previous_data is None:
                previous_data = transformed_data
                yield transformed_data
            else:
                if transformed_data != previous_data:
                    previous_data = transformed_data
                    yield transformed_data
                else:
                    yield []
        except requests.HTTPError as http_err:
            if http_err.response.status_code == 429:
                logging.warning("Rate limit hit (429), backing off for %s seconds", backoff_time)
                time.sleep(backoff_time)
                backoff_time = min(backoff_time * 2, max_backoff)
                yield None
            else:
                logging.error("HTTP error, yielding None: %s", http_err)
                yield None
        except Exception as e:
            logging.error("Error in stream_fraudguard_data: %s", e)
            yield None
        time.sleep(interval)

if __name__ == "__main__":
    print("Starting continuous streaming every 10 seconds (Ctrl+C to stop)...")
    try:
        for i, data in enumerate(stream_fraudguard_data(interval=10)):
            print(f"\nStream batch {i + 1}:")
            if data is None:
                print("No data retrieved from Fraudguard API")
            elif data:
                print("New or changed records:")
                print(json.dumps(data, indent=4))
                print(f"Total new/changed records: {len(data)}")
            else:
                print("No new or changed records since last batch.")
    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")
    except Exception as e:
        print(f"Error during streaming: {e}")
