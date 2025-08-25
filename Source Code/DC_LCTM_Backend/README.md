# Live Cyber Threat Map - Backend

The backend of the Live Cyber Threat Map is a Flask-based asynchronous data engine that collects, processes, and serves real-time cyber threat intelligence. It aggregates data from multiple public sources including live attack feeds, malicious IP blocklists, and cybersecurity news, and exposes them through REST and SSE APIs for visualization.

---

## Features

- Asynchronous threat data collection (FortiGuard, Radware)
- Malicious IP aggregation (AlienVault, BinaryDefense, FraudGuard, Talos)
- Cybersecurity news filtering (HackerNews, DarkReading, 420.in RSS)
- Modular architecture to easily add more sources
- Geolocation via MaxMind GeoLite2
- REST and SSE API endpoints: `/threats`, `/news`, `/malicious-ips`
- Built-in deduplication, grouping, retry logic, and resilient error handling

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
cd DC_LCTM_Backend
pip install -r requirements.txt
````

### Running the Server

#### Development

```bash
python server.py
```

#### Production (Recommended)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

---

## API Endpoints

* `/threats` – Real-time threat data via Server-Sent Events (SSE)
* `/news` – Latest filtered cybersecurity news (JSON)
* `/malicious-ips` – Geolocated malicious IPs (JSON)

---

## Project Structure

```
Backend/
├─ assets/
│  ├─ country_coordinates.json   # Centroid data for country-level mapping
│  └─ GeoLite2-City.mmdb         # MaxMind IP geolocation database
├─ templates/
│  └─ index.html                 # Optional fallback/test UI
├─ cyber_threat_intel.py        # Asynchronous data collection and processing logic
├─ requirements.txt             # Python dependency list
└─ server.py                    # Flask server with REST/SSE routes
```

---