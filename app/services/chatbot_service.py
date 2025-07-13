import os
from dotenv import load_dotenv
import openai
os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

API_KEY = os.getenv("NCLOVA_API_KEY")
API_URL = "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003"

HEADERS = {
    "X-NCP-CLOVASTUDIO-API-KEY": API_KEY,
    "X-NCP-APIGW-API-KEY": API_KEY,
    "Content-Type": "application/json",
}

session_store = {}

# CLOVA 활용 채팅
def get_chatbot_response_clova(session_id: str, user_message: str) -> str:
    if session_id not in session_store:
        session_store[session_id] = [
            {"role": "system", "content": "너는 Wisemind의 투자 분석 도우미야. 간결하고 정확하게 답변해."}
        ]

    conversation = session_store[session_id]
    conversation.append({"role": "user", "content": user_message})

    try:
        payload = {
            "messages": conversation,
            "topP": 0.8,
            "topK": 0,
            "temperature": 0.7,
            "repeatPenalty": 5.0,
            "stopBefore": [],
            "includeAiFilters": False,
            "seed": 0,
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        assistant_reply = response.json()["result"]["message"]["content"].strip()

        conversation.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply

    except Exception as e:
        print(f"HyperCLOVA X Error: {e}")
        return "답변 생성 실패"



client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

#OpenAI 활용 채팅
def get_chatbot_response(session_id: str, user_message: str) -> str:
    if session_id not in session_store:
        session_store[session_id] = [
            {"role": "system", "content": "너는 Wisemind의 투자 분석 도우미야. 간결하고 정확하게 답변해."}
        ]

    conversation = session_store[session_id]
    conversation.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
        )
        assistant_reply = response.choices[0].message.content.strip()
        conversation.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return "답변 생성 실패"

def reset_chatbot_session(session_id: str):
    if session_id in session_store:
        del session_store[session_id]
        return True
    return False
