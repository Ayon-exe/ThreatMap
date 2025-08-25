import feedparser
import json
import os
import re

RSS_FEED_URL = "https://www.darkreading.com/rss.xml"

PRIMARY_KEYWORDS = [
    "ransomware", "malware", "exploit", "vulnerability", "breach", 
    "zero-day", "attack", "compromised", "infected", "stolen", 
    "hacked", "leak", "backdoor", "trojan", "rootkit", "spyware"
]

SECONDARY_KEYWORDS = [
    "cybercrime", "phishing", "ddos", "apt", "hacking", "credential",
    "cyberattack", "databreach", "hack", "payload", "threat", "botnet",
    "mitigation", "critical", "authentication", "attacker", "command and control",
    "lateral movement", "exfiltration", "intrusion", "security flaw"
]

EXCLUDE_TERMS = [
    "webinar", "workshop", "training", "course", "certification", 
    "conference", "roundtable", "partner", "sponsored", "promotion",
    "discount", "offer", "register now", "sign up", "earn", "sale",
    "subscription", "tutorial", "guide", "how to", "introduction to"
]

SEEN_LINKS_FILE = "seen_darkreading.json"
DEBUG = False

def load_seen_links():
    if not os.path.exists(SEEN_LINKS_FILE):
        return set()
    try:
        with open(SEEN_LINKS_FILE, "r") as f:
            return set(json.load(f))
    except (json.JSONDecodeError, FileNotFoundError):
        return set()

def save_seen_links(seen_links):
    with open(SEEN_LINKS_FILE, "w") as f:
        json.dump(list(seen_links), f)

def is_relevant_article(title, text):
    for term in EXCLUDE_TERMS:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            return False, []
    
    primary_matches = [kw for kw in PRIMARY_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE)]
    if not primary_matches:
        return False, []
    
    secondary_matches = [kw for kw in SECONDARY_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE)]
    return True, primary_matches + secondary_matches

def fetch_threat_news():
    seen_links = load_seen_links()
    feed = feedparser.parse(RSS_FEED_URL)
    filtered_articles = []

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        summary = entry.get("summary", "") or entry.get("description", "")
        summary = summary.strip()
        link = entry.get("link", "").strip()
        published = entry.get("published", "Unknown Timestamp")

        if not title or not link:
            continue

        text = f"{title} {summary}"
        is_relevant, matches = is_relevant_article(title, text)

        if is_relevant and link not in seen_links:
            article = {
                "title": title,
                "link": link,
                "timestamp": published
            }
            filtered_articles.append(article)
            seen_links.add(link)

            if DEBUG:
                print(f"[RELEVANT] {title}")
                print(f"Keywords: {', '.join(matches)}")
                print(f"Link: {link}")
                print("-" * 50)

    save_seen_links(seen_links)
    return filtered_articles

if __name__ == "__main__":
    news_list = fetch_threat_news()
    news_list.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    print(json.dumps(news_list, indent=2))
