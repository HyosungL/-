import os
import requests
from datetime import datetime, timedelta

# 환경 변수에서 API 키와 데이터베이스 ID를 가져옵니다.
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Notion API 설정
NOTION_API_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2021-05-13",
    "Content-Type": "application/json"
}

# 데이터베이스에서 데이터 가져오기
response = requests.post(NOTION_API_URL, headers=headers)
data = response.json()

# 날짜 비교하기
def check_and_update():
    for result in data["results"]:
        last_edited_time = result['properties']['마지막업로드']['date']['start']
        last_edited_date = datetime.strptime(last_edited_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        two_days_ago = datetime.now() - timedelta(days=2)
        
        if last_edited_date < two_days_ago:
            page_id = result['id']
            update_notion_page(page_id)

def update_notion_page(page_id):
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    update_data = {
        "properties": {
            "업로드한 채널": {
                "multi_select": []  # 다중 선택 항목 초기화
            },
            "상태": {
                "select": {
                    "name": "가능"  # 상태를 "가능"으로 변경
                }
            }
        }
    }
    
    response = requests.patch(update_url, headers=headers, json=update_data)
    if response.status_code == 200:
        print(f"페이지 {page_id} 업데이트 성공!")
    else:
        print(f"페이지 {page_id} 업데이트 실패: {response.status_code}")

check_and_update()
