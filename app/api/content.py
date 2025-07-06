from fastapi import APIRouter, Query
from app.services.news_service import get_news
from app.services.article_service import extract_article_content, get_embedding
from app.services.generator_service import generate_level_articles
from app.services.storage_service import save_article_to_nest

router = APIRouter()

@router.get("/generate-articles")
def generate_articles(q: str = Query(...)):
    news_list = get_news(q)[:5]
    all_texts = []
    source_links = []

    for news in news_list:
        try:
            url = news["link"]
            full_text = extract_article_content(url)
            all_texts.append(full_text)
            source_links.append(url)
        except Exception as e:
            print(f"본문 크롤링 에러: {e}")
            continue

    if len(all_texts) < 3:
        return {"message": "충분한 뉴스 데이터를 수집하지 못했습니다."}

    articles = generate_level_articles(all_texts, q)
    results = {}

    for level, content in articles.items():
        vector = get_embedding(content)
        record = {
            "topic": q,
            "difficulty": level,
            "article": content,
            "vector": vector,
            "sources": source_links
        }
        save_article_to_nest(record)
        print(f"{level} 아티클 저장 완료")

        results[level] = {
            "article": content,
            "vector_dim": len(vector),
            "vector": vector,
            "sources": source_links
        }

    return {
        "topic": q,
        "results": results
    }
