import re
import requests
from ipaddress import ip_address

def fetch_and_process_malicious_ips():

    # Constants
    ALIEN_URL = 'https://reputation.alienvault.com/reputation.unix'
    BD_BANLIST_URL = 'https://www.binarydefense.com/banlist.txt'
    BD_TORLIST_URL = 'https://www.binarydefense.com/tor.txt'
    IP_CANDIDATE_REGEX = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    def is_valid_ip(ip_str):
        try:
            ip_address(ip_str)
            return True
        except ValueError:
            return False

    def extract_ips(data):
        return sorted(set(ip for ip in IP_CANDIDATE_REGEX.findall(data) if is_valid_ip(ip)))

    def download_url(url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return ""

    all_ips = set()

    # BinaryDefense Banlist
    banlist_data = download_url(BD_BANLIST_URL)
    banlist_ips = extract_ips(banlist_data)
    all_ips.update(banlist_ips)

    # BinaryDefense TOR list
    torlist_data = download_url(BD_TORLIST_URL)
    torlist_ips = extract_ips(torlist_data)
    all_ips.update(torlist_ips)

    # AlienVault Reputation
    otx_data = download_url(ALIEN_URL)
    otx_ips = extract_ips(otx_data)
    all_ips.update(otx_ips)

    # Combine and export
    final_list = sorted(all_ips)

    return final_list

# Run on execution
if __name__ == "__main__":
    print(fetch_and_process_malicious_ips())
