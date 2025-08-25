import requests
import json

def stream_threat_data():
    """
    Stream threat data from Check Point's ThreatMap API.
    Yields:
        Dict: A unique threat data dictionary as it arrives.
    """
    url = 'https://threatmap-api.checkpoint.com/ThreatMap/api/feed'
    headers = {
        'Accept': 'text/event-stream',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'threatmap-api.checkpoint.com',
        'Origin': 'https://threatmap.checkpoint.com',
        'Referer': 'https://threatmap.checkpoint.com/',
        'User-Agent': 'Mozilla/5.0'
    }

    seen_records = set()

    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data:"):
                        try:
                            json_data = json.loads(decoded_line[5:])
                            threat_data = {}
                            mapping = {
                                "a_c": "Attack Count",
                                "a_n": "Attack Name",
                                "a_t": "Attack Type",
                                "d_co": "Destination Country Code",
                                "d_la": "Destination Latitude",
                                "d_lo": "Destination Longitude",
                                "d_s": "Destination Severity",
                                "s_co": "Source Country Code",
                                "s_lo": "Source Longitude",
                                "s_la": "Source Latitude",
                                "s_s": "Source Severity",
                                "t": "Timestamp"
                            }

                            for key, label in mapping.items():
                                value = json_data.get(key)
                                if value not in [None, "None"]:
                                    threat_data[label] = value

                            if threat_data:
                                record_tuple = tuple(threat_data.items())
                                if record_tuple not in seen_records:
                                    seen_records.add(record_tuple)
                                    yield threat_data

                        except json.JSONDecodeError:
                            continue
    except Exception:
        pass


# Show live streaming data when run directly
if __name__ == "__main__":
    for threat in stream_threat_data():
        print(threat)
