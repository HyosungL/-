import os
import requests
from datetime import datetime, timedelta

# 환경 변수에서 Notion API Key와 Database ID를 가져옵니다.
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Notion API URL 설정
NOTION_API_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2021-05-13",
    "Content-Type": "application/json"
}

# 데이터베이스에서 데이터를 가져오는 요청을 보냅니다.
response = requests.post(NOTION_API_URL, headers=headers)
data = response.json()

# 응답 출력 (디버깅용)
print(data)

# 날짜 비교하고 업데이트하기
def check_and_update():
    for result in data.get("results", []):  # results 키가 없을 경우 빈 리스트로 처리
        last_edited_time = result['properties']['마지막업로드']['date']['start']
        last_edited_date = datetime.strptime(last_edited_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        two_days_ago = datetime.now() - timedelta(days=2)
        
        # 마지막업로드가 2일 이상이면 업데이트
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
    
    # Notion API 요청을 보내 페이지 업데이트
    response = requests.patch(update_url, headers=headers, json=update_data)
    if response.status_code == 200:
        print(f"페이지 {page_id} 업데이트 성공!")
    else:
        print(f"페이지 {page_id} 업데이트 실패: {response.status_code}")

# 날짜 비교 및 업데이트 함수 실행
check_and_update()
