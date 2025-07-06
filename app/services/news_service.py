import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_news(query: str, display: int = 5):
    url = "https://openapi.naver.com/v1/search/news"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {"query": query, "display": display, "sort": "sim"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"뉴스 요청 실패: {response.status_code} - {response.text}")

    items = response.json().get("items", [])
    cleaned_items = []

    for item in items:
        cleaned_items.append({
            "title": clean_html(item["title"]),
            "description": clean_html(item["description"]),
            "link": item["link"],
            "pubDate": item["pubDate"]
        })

    return cleaned_items

def clean_html(raw_text: str) -> str:
    cleaner = re.compile('<.*?>')
    return re.sub(cleaner, '', raw_text)