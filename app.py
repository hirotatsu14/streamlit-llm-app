from dotenv import load_dotenv

load_dotenv()


from dotenv import load_dotenv
import os
import streamlit as st
# コミュニティ版LangChainからインポート
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .env または Streamlit Secrets 経由で API キーを読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# LLMインスタンスを生成
llm = ChatOpenAI(
    api_key=api_key,
    model_name="gpt-3.5-turbo"
)

# LLMへの問い合わせ関数
def get_response(role: str, user_input: str) -> str:
    system_msg = f"あなたは{role}として振る舞ってください。"
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=user_input),
    ]
    return llm(messages).content

# Streamlit UI
st.title("LLM専門家チャットアプリ")
st.write("選択した専門家になりきって、あなたの質問に回答します。")

role = st.radio(
    "専門家を選択してください：", ["医師", "弁護士", "エンジニア"]
)

user_input = st.text_input("質問を入力してください。")

if st.button("送信"):
    if user_input:
        with st.spinner("応答中..."):
            response = get_response(role, user_input)
            st.success(response)
    else:
        st.warning("質問を入力してください。")
