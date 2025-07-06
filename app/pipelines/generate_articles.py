from app.services.news_service import get_news
from app.services.article_service import extract_article_content, get_embedding
from app.services.generator_service import generate_level_articles
from app.services.storage_service import save_article_to_nest

def run_generation(topic: str):
    news_list = get_news(topic)[:5]
    all_texts = []
    source_links = []

    for item in news_list:
        try:
            text = extract_article_content(item["link"])
            all_texts.append(text)
            source_links.append(item["link"])
        except:
            continue

    if len(all_texts) < 3:
        print("충분한 뉴스 데이터 부족")
        return

    articles = generate_level_articles(all_texts, topic)

    for level, content in articles.items():
        vector = get_embedding(content)
        record = {
            "topic": topic,
            "difficulty": level,
            "article": content,
            "vector": vector,
            "sources": source_links
        }
        save_article_to_nest(record)
        print(f"{level} 아티클 저장 완료")
