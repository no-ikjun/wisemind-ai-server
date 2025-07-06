import openai
import os
from dotenv import load_dotenv
import re

load_dotenv()
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

def generate_level_articles(all_texts: list, topic: str) -> dict:
    combined_text = "\n\n".join(all_texts)

    prompt = f"""
    다음은 '{topic}' 주제의 뉴스 5개 내용입니다:

    \"\"\"{combined_text}\"\"\"

    이 정보를 바탕으로 투자자를 위한 Wisemind 아티클을 난이도별로 3개 작성해줘.

    조건:
    - 초급 투자자용 (beginner)
    - 중급 투자자용 (intermediate)
    - 고급 투자자용 (advanced)

    각 아티클에는 반드시 다음을 포함해야 함:
    - 최신 투자 동향과 시장 상황
    - 해당 주제 관련 주요 기업의 움직임 및 발표
    - 전문가의 해석 또는 전망 (AI가 상상력으로 작성 가능)
    - 투자자가 실질적으로 고려해야 할 포인트
    - 전체 분량: 최소 1000자 이상, 최대 2000자 이내

    초급은 쉽게, 고급은 심도 깊게 작성해야 하며, 각 수준에 맞는 전문 용어와 배경 설명을 조정해야 함.

    !!IMPORTANT!!!형식은 반드시 다음을 준수:
    [Beginner]
    (초급 아티클 본문)

    [Intermediate]
    (중급 아티클 본문)

    [Advanced]
    (고급 아티클 본문)
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000
    )

    content = response.choices[0].message.content.strip()
    return parse_level_output(content)


def parse_level_output(output: str) -> dict:
    result = {"beginner": "", "intermediate": "", "advanced": ""}

    beginner_match = re.search(r"\[Beginner\](.*?)(?=\[Intermediate\]|\[Advanced\]|$)", output, re.DOTALL)
    intermediate_match = re.search(r"\[Intermediate\](.*?)(?=\[Advanced\]|$)", output, re.DOTALL)
    advanced_match = re.search(r"\[Advanced\](.*)", output, re.DOTALL)

    if beginner_match:
        result["beginner"] = beginner_match.group(1).strip()
    if intermediate_match:
        result["intermediate"] = intermediate_match.group(1).strip()
    if advanced_match:
        result["advanced"] = advanced_match.group(1).strip()

    return result
