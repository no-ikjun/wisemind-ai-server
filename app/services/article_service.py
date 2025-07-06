from newspaper import Article
from sentence_transformers import SentenceTransformer
import requests
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

NCLOVA_API_URL = os.getenv("NCLOVA_URL") + "/v1/api-tools/embedding/v2"
NCLOVA_API_KEY = os.getenv("NCLOVA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_article_content(url: str) -> str:
    article = Article(url, language='ko')
    article.download()
    article.parse()
    return article.text

# def get_embedding(text: str):
#     """Naver Clova 활용 임베딩"""
#     headers = {
#         "Authorization": f"Bearer {NCLOVA_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {"texts": [text]}

#     response = requests.post(NCLOVA_API_URL, headers=headers, json=payload)
#     if response.status_code == 200:
#         return response.json()["results"][0]["embedding"]
#     else:
#         raise Exception(f"Embedding 요청 실패: {response.text}")
    
def get_embedding(text: str):
    sentences = text.split('. ') # 문장 단위 분리
    embeddings = model.encode(sentences, convert_to_tensor=True)
    vector = np.mean(embeddings.cpu().numpy(), axis=0)
    return vector.tolist()