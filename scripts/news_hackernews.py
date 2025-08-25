import feedparser
import json
import os
import re

# ------------------- Configuration -------------------

RSS_FEED_URL = "https://feeds.feedburner.com/TheHackersNews"

# Primary security incident keywords - these are required for a match
PRIMARY_KEYWORDS = [
    "ransomware", "malware", "exploit", "vulnerability", "breach", 
    "zero-day", "attack", "compromised", "infected", "stolen", 
    "hacked", "leak", "backdoor", "trojan", "rootkit", "spyware"
]

# Secondary keywords - these add context but at least one primary is required
SECONDARY_KEYWORDS = [
    "cybercrime", "phishing", "ddos", "apt", "hacking", "credential",
    "cyberattack", "databreach", "hack", "payload", "threat", "botnet",
    "mitigation", "critical", "authentication", "attacker", "command and control",
    "lateral movement", "exfiltration", "intrusion", "security flaw"
]

# Exclusion terms - if these appear in the title, exclude the article
EXCLUDE_TERMS = [
    "webinar", "workshop", "training", "course", "certification", 
    "conference", "roundtable", "partner", "sponsored", "promotion",
    "discount", "offer", "register now", "sign up", "earn", "sale",
    "subscription", "tutorial", "guide", "how to", "introduction to"
]

SEEN_LINKS_FILE = "seen_hackernews.json"
DEBUG = False  # Set True to print matches

# ------------------- Utilities -------------------

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
    """Determine if an article is relevant based on keywords and exclusions"""
    
    # Check for exclusion terms first
    for term in EXCLUDE_TERMS:
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            return False, []
    
    # Check for primary keywords
    primary_matches = []
    for keyword in PRIMARY_KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            primary_matches.append(keyword)
    
    # Must have at least one primary keyword
    if not primary_matches:
        return False, []
    
    # Check for secondary keywords
    secondary_matches = []
    for keyword in SECONDARY_KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            secondary_matches.append(keyword)
    
    # Combine matches
    all_matches = primary_matches + secondary_matches
    
    # Return True if we have matches and no exclusions
    return len(all_matches) > 0, all_matches

# ------------------- Main Function -------------------

def fetch_threat_news():
    seen_links = load_seen_links()
    feed = feedparser.parse(RSS_FEED_URL)
    filtered_articles = []
    
    for entry in feed.entries:
        title = entry.get("title", "").strip()
        # Get summary from either summary or description field
        summary = entry.get("summary", "") or entry.get("description", "")
        summary = summary.strip()
        link = entry.get("link", "").strip()
        published = entry.get("published", "Unknown Timestamp")
        
        if not title or not link:
            continue
        
        # Combine title and summary for matching
        text = f"{title} {summary}"
        
        # Check if article is relevant
        is_relevant, matches = is_relevant_article(title, text)
        
        if is_relevant and link not in seen_links:
            # Extract the date for easier sorting
            date_match = re.search(r'\w+, (\d+ \w+ \d+)', published)
            date_str = date_match.group(1) if date_match else "Unknown Date"
            
            article = {
                "title": title,
                "link": link,
                "timestamp": published,
                "date": date_str
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

# ------------------- Example Usage -------------------

if __name__ == "__main__":
    news_list = fetch_threat_news()
    
    # Sort by date (newest first)
    news_list.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # For json output
    print(json.dumps(news_list, indent=2))