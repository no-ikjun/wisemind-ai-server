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
    for dist, idx in zip(D[0], I[0]):
        if idx >= len(metadata):
            continue

        relevance_score = (1 - (float(dist) / float(max_dist))) * 100
        relevance_score = max(0, min(100, relevance_score))

        item = metadata[idx].copy() if isinstance(metadata[idx], dict) else dict(metadata[idx])
        item["relevance"] = round(float(relevance_score), 1)
        results.append(item)

    # 부족분 랜덤 채우기
    if len(results) < top_k:
        all_articles = get_all_articles()
        remaining = [a for a in all_articles if a not in results]
        import random
        random.shuffle(remaining)
        results.extend(remaining[:top_k - len(results)])

    return results[:top_k]
