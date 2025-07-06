import os
import openai
os.environ["TOKENIZERS_PARALLELISM"] = "false"

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

session_store = {}

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