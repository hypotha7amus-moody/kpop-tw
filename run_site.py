import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_kktix():
    print("正在抓取 KKTIX...")
    url = "https://kktix.com/events?search=%E9%9F%93"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
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
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        events = []
        for item in soup.select('.thumbnail'):
            title_el = item.select_one('h2')
            title = title_el.text.strip() if title_el else ""
            if any(k in title for k in ["韓", "Korea", "Fan Meeting", "Tour", "LIVE", "ASIA"]):
                link_el = item.select_one('a')
                link = "https://tixcraft.com" + link_el['href'] if link_el else "#"
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
    url = "https://ticketplus.com.tw/search?q=%E9%9F%93"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        events = []
        # 遠大的結構檢索
        for card in soup.select('.v-card'):
            title_el = card.select_one('.v-card__title')
            link_el = card.find('a')
            if title_el and link_el:
                title = title_el.text.strip()
                link = "https://ticketplus.com.tw" + link_el['href']
                events.append({
                    "date": "見官網",
                    "group": title,
                    "link": link,
                    "source": "遠大售票"
                })
        return events
    except Exception as e:
        print(f"遠大失敗: {e}"); return []

def update_all():
    all_data = []
    all_data.extend(fetch_kktix())
    all_data.extend(fetch_tixcraft())
    all_data.extend(fetch_ticketplus())
    
    exclude_keywords = ["課程", "料理", "韓語", "留學", "演講"]
    final_data = []
    seen_titles = set()
    
    for e in all_data:
        # 去重與過濾雜訊
        if e['group'] not in seen_titles and not any(ex in e['group'] for ex in exclude_keywords):
            final_data.append(e)
            seen_titles.add(e['group'])
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(f"const kpopData = {json.dumps(final_data, ensure_ascii=False)};")
    print(f"全部更新完成！共抓取 {len(final_data)} 筆資料。")

if __name__ == "__main__":
    update_all()
