from dotenv import load_dotenv

load_dotenv()


from dotenv import load_dotenv
import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数ロード
load_dotenv()
# APIキー取得
api_key = os.getenv("OPENAI_API_KEY")

# LLM初期化（プロキシ自動注入をキャンセル）
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-3.5-turbo",
    openai_proxy=None,
)

# LLM呼び出し関数
def get_response(role: str, user_input: str) -> str:
    system_msg = f"あなたは{role}として振る舞ってください。"
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=user_input),
    ]
    return llm(messages).content

# Streamlit UI
st.title("LLM専門家チャットアプリ")
st.write("入力した質問に対して、選んだ専門家になりきって回答してくれます。")

# 専門家選択
role = st.radio(
    "専門家を選択してください：", ["医師", "弁護士", "エンジニア"]
)

# 質問入力
user_input = st.text_input("質問を入力してください")

# 送信ボタン
if st.button("送信"):
    if user_input:
        with st.spinner("応答中..."):
            response = get_response(role, user_input)
            st.success(response)
    else:
        st.warning("質問を入力してください。")
