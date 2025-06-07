from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def get_llm_response(input_text: str, expert_type: str) -> str:
    """
    ユーザー入力と専門家タイプをもとにLLMへ問い合わせ、
    生成された回答を返します。

    Args:
        input_text (str): ユーザーの質問
        expert_type (str): 選択した専門家タイプ

    Returns:
        str: LLMの回答（エラー時はエラーメッセージ）
    """
    # APIキー取得
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        return (
            "エラー：OpenAI APIキーが設定されていません。\n"
            "環境変数またはStreamlit SecretsにOPENAI_API_KEYを登録してください。"
        )

    # 専門家ごとのシステムメッセージ
    system_messages = {
        "データサイエンティスト": (
            "あなたはベテランのデータサイエンティストです。"
            "統計学、機械学習、データ分析に精通しており、"
            "初心者にもわかりやすく説明してください。"
        ),
        "マーケティング戦略家": (
            "あなたは熟練したマーケティング戦略家です。"
            "ブランド戦略、デジタルマーケティング、市場調査の知見を活かし、"
            "ROIを重視した提案を行ってください。"
        )
    }

    try:
        llm = ChatOpenAI(
            openai_api_key=api_key,
            model_name="gpt-4o-mini",
            temperature=0.7
        )
        messages = [
            SystemMessage(content=system_messages[expert_type]),
            HumanMessage(content=input_text)
        ]
        result = llm(messages)
        return result.content

    except Exception as e:
        return f"エラーが発生しました: {e}"

def main():
    # ページ設定
    st.set_page_config(
        page_title="ビジネスAIアシスタント",
        layout="wide"
    )

    # タイトルと概要
    st.title("ビジネスAIアシスタント")
    st.markdown("---")
    st.markdown(
        "このアプリは、選択した専門家としてAIが回答を提供します。\n"
        "質問内容を入力し、最下部の「回答を取得」ボタンを押してください。"
    )
    st.markdown("---")

    # レイアウト：設定欄と入力欄
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("設定")
        expert_type = st.radio(
            "専門家を選択",
            ["データサイエンティスト", "マーケティング戦略家"]
        )
        descriptions = {
            "データサイエンティスト": "データ分析と機械学習の専門家",
            "マーケティング戦略家": "市場調査と戦略立案の専門家"
        }
        st.info(descriptions[expert_type])

    with col2:
        st.subheader("質問入力")
        input_text = st.text_area(
            "質問内容を入力してください",
            height=150
        )
        if st.button("回答を取得"):
            if input_text.strip():
                with st.spinner("回答を生成しています..."):
                    answer = get_llm_response(input_text, expert_type)
                st.subheader("回答")
                st.write(answer)
            else:
                st.warning("質問内容を入力してください。")

    # フッター
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:gray;'>"
        "<small>Powered by LangChain & OpenAI</small>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
