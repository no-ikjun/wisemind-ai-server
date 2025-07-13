from fastapi import APIRouter, Body
from app.services.vector_db_service import get_index, get_all_articles
from app.services.article_service import get_embedding
import numpy as np

router = APIRouter()

@router.post("/articles")
def recommend(data: dict = Body(...)):
    index = get_index()
    metadata = get_all_articles()

    query_text = f"{data['interests']} {data['riskProfile']} {data['knowledgeLevel']}"
    query_vec = get_embedding(query_text)

    top_k = data.get("limit", 15)
    D, I = index.search(np.array([query_vec], dtype="float32"), top_k)

    max_dist = max(D[0]) if max(D[0]) > 0 else 1

    results = []
    used_titles = set()

    for dist, idx in zip(D[0], I[0]):
        if idx >= len(metadata):
            continue

        item = metadata[idx].copy() if isinstance(metadata[idx], dict) else dict(metadata[idx])
        title = item.get("topic") or item.get("title") or ""

        if title in used_titles:
            continue

        relevance_score = (1 - (float(dist) / float(max_dist))) * 100
        relevance_score = max(0, min(100, relevance_score))
        item["relevance"] = round(float(relevance_score), 1)

        results.append(item)
        used_titles.add(title)

    # 부족분 랜덤 채우기 (중복 제거 포함)
    if len(results) < top_k:
        all_articles = get_all_articles()
        import random
        random.shuffle(all_articles)

        for article in all_articles:
            title = article.get("topic") or article.get("title") or ""
            if title not in used_titles:
                article = article.copy() if isinstance(article, dict) else dict(article)
                article["relevance"] = 0  # 랜덤 채운 건 relevance 없음
                results.append(article)
                used_titles.add(title)
                if len(results) >= top_k:
                    break

    return results[:top_k]
