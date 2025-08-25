import requests
import json
import time

API_KEY = "63303b5b42a8deb9aaa006a925cc5b4e3b6a865b54cc64840c5a98ae2a0e2643e0211df38481b5bc"
API_URL = "https://api.abuseipdb.com/api/v2/check"

IP_LIST = [
    "8.8.8.8",
    "1.1.1.1",
    "185.232.67.74",  # Sample malicious IP
]

HEADERS = {
    "Accept": "application/json",
    "Key": API_KEY
}

def query_abuseipdb(ip, max_age=90):
    params = {
        "ipAddress": ip,
        "maxAgeInDays": max_age
    }
    try:
        print(f"\n[>] Querying IP: {ip}")
        response = requests.get(API_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
        return data
    except requests.exceptions.HTTPError as e:
        print(f"[!] HTTP Error: {e}")
    except Exception as e:
        print(f"[!] General Error: {e}")
    time.sleep(1)  # Respect AbuseIPDB rate limits

def run():
    for ip in IP_LIST:
        query_abuseipdb(ip)

if __name__ == "__main__":
    run()
