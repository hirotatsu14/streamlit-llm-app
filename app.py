from dotenv import load_dotenv

load_dotenv()


import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    api_key=api_key,  # ここを openai_api_key→api_key に修正！
    model="gpt-3.5-turbo"
)

def get_response(role, user_input):
    system_msg = f"あなたは{role}として振る舞ってください。"
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=user_input)
    ]
    return llm(messages).content

st.title("LLM専門家チャットアプリ")
st.write("入力した質問に対して、選んだ専門家になりきって回答してくれます。")
role = st.radio("専門家を選択してください：", ["医師", "弁護士", "エンジニア"])
user_input = st.text_input("質問を入力してください")

if st.button("送信"):
    if user_input:
        with st.spinner("応答中..."):
            response = get_response(role, user_input)
            st.success(response)
    else:
        st.warning("質問を入力してください。")
