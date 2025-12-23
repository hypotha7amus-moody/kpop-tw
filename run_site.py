import requests
from bs4 import BeautifulSoup
import json

def update_data():
    # 這是搜尋 KKTIX 上「韓」相關的活動
    url = "https://kktix.com/events?search=%E9%9F%93"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    print("正在抓取 KKTIX 最新行程...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    events = soup.select('.event-unit')
    
    results = []
    for event in events:
        title = event.select_one('.event-title').text.strip()
        # 我們只抓取看起來像女團或演唱會的關鍵字 (你可以自行擴充)
        results.append({
            "date": event.select_one('.date').text.strip(),
            "group": title,
            "link": event.select_one('a')['href']
        })
    
    # 將抓到的資料存成 data.js，讓 HTML 網頁可以直接讀取
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(f"const kpopData = {json.dumps(results, ensure_ascii=False)};")
    
    print(f"成功抓取 {len(results)} 筆資料，並更新到 data.js！")

if __name__ == "__main__":
    update_data()