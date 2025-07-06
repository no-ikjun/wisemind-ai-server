import requests
import os
from app.services.vector_db_service import add_vector

def save_vector_to_local_db(vector: list, meta: dict):
    add_vector(vector, meta)
    print("벡터 DB에 저장 완료")


NEST_API_URL = os.getenv("NEST_API_URL")
# NEST_API_URL = "http://localhost:5050"

def save_article_to_nest(payload: dict):
    try:
        response = requests.post(f"{NEST_API_URL}/articles", json=payload)
        if response.status_code == 201:
            print("아티클 저장 완료")
        else:
            print(f"저장 실패: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"요청 중 에러 발생: {e}")
