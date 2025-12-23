import requests
import json
import csv

# 【在此替換你的 Google Sheet ID】
SHEET_ID = "1Fvh2HK-DmD_n4tQHtP6JWQaQnyf5R68jHJ6vE8qnyr8"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/1Fvh2HK-DmD_n4tQHtP6JWQaQnyf5R68jHJ6vE8qnyr8/gviz/tq?tqx=out:csv"

def fetch_from_sheet():
    print("正在從 Google Sheet 抓取資料...")
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        # 使用 CSV 格式解析
        lines = response.text.splitlines()
        reader = csv.DictReader(lines)
        
        events = []
        for row in reader:
            events.append({
                "date": row['date'],
                "group": row['group'],
                "link": row['link'],
                "source": row['source']
            })
        return events
    except Exception as e:
        print(f"抓取失敗: {e}")
        return []

def update_all():
    final_data = fetch_from_sheet()
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(f"const kpopData = {json.dumps(final_data, ensure_ascii=False)};")
    print(f"更新完成，共 {len(final_data)} 筆。")

if __name__ == "__main__":
    update_all()
