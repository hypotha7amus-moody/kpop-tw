import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_kktix():
    print("正在抓取 KKTIX...")
    url = "https://kktix.com/events?search=%E9%9F%93"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        events = []
        for event in soup.select('.event-unit'):
            title = event.select_one('.event-title').text.strip()
            events.append({
                "date": event.select_one('.date').text.strip(),
                "group": title,
                "link": event.select_one('a')['href'],
                "source": "KKTIX"
            })
        return events
    except Exception as e:
        print(f"KKTIX 失敗: {e}"); return []

def fetch_tixcraft():
    print("正在抓取 拓元...")
    url = "https://tixcraft.com/activity"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        events = []
        for item in soup.select('.thumbnail'):
            title = item.select_one('h2').text.strip() if item.select_one('h2') else ""
            if any(k in title for k in ["韓", "Korea", "Fan Meeting", "Tour", "LIVE"]):
                link = "https://tixcraft.com" + item.select_one('a')['href']
                events.append({
                    "date": "見官網", 
                    "group": title,
                    "link": link,
                    "source": "拓元售票"
                })
        return events
    except Exception as e:
        print(f"拓元失敗: {e}"); return []

def fetch_ticketplus():
    print("正在抓取 遠大 (Ticket Plus)...")
    # 遠大搜尋「韓」的連結
    url = "https://ticketplus.com.tw/search?q=%E9%9F%93"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        events = []
        # 遠大的結構通常在 .v-card 中
        for card in soup.select('.v-card'):
            title_el = card.select_one('.v-card__title')
            if title_el:
                title = title_el.text.strip()
                link = "https://ticketplus
