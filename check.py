import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://wwwi2.ymparisto.fi/i2/14/q1410400y/wqfi.html"
THRESHOLD = 115

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def get_flow():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    match = re.search(r"Virtaama.*?(\d+,\d+|\d+\.\d+|\d+)", text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None

flow = get_flow()

if flow and flow > THRESHOLD:
    send(f"⚠️ Pernoonkoski flow is {flow} m³/s (above 115)")
