from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def get_llm_response(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # OpenAI APIキーの設定
    openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    
    if not openai_api_key:
        return "Error: OpenAI APIキーが設定されていません。環境変数またはStreamlit secretsでOPENAI_API_KEYを設定してください。"
    
    # 専門家タイプに応じたシステムメッセージの設定
    system_messages = {
        "データサイエンティスト": """あなたは経験豊富なデータサイエンティストです。
        統計学、機械学習、データ分析、データ可視化に関する深い知識を持っています。
        技術的な質問に対しては具体的で実用的なアドバイスを提供し、
        初心者にも分かりやすく説明することを心がけてください。
        Pythonやデータ分析ライブラリ（pandas、numpy、scikit-learn等）の活用方法も熟知しています。""",

        "マーケティング戦略家": """あなたは経験豊富なマーケティング戦略家です。
        ブランド戦略、デジタルマーケティング、消費者行動分析、市場調査に関する深い知識を持っています。
        実践的で効果的なマーケティング施策を提案し、
        ROIを重視した戦略的思考でアドバイスを提供してください。
        最新のマーケティングトレンドやツールの活用方法も熟知しています。"""
    }
    
    try:
        # ChatOpenAIモデルの初期化
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=openai_api_key
        )
        
        # メッセージの作成
        messages = [
            SystemMessage(content=system_messages[expert_type]),
            HumanMessage(content=input_text)
        ]
        
        # LLMからの回答を取得
        response = llm(messages)
        return response.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


def main():
    # ページ設定
    st.set_page_config(
        page_title="AI専門家アシスタント",
        page_icon="🤖",
        layout="wide"
    )
    
    # タイトル
    st.title("🤖 AI専門家アシスタント")
    st.markdown("---")
    
    # アプリの概要説明
    st.markdown("""
    ## 📖 アプリの概要
    このWebアプリは、LangChainを使用してLLMと対話できるアシスタントツールです。
    異なる専門分野の専門家として振る舞うAIに質問や相談をすることができます。
    
    ## 🚀 使用方法
    1. **専門家の選択**: ラジオボタンから相談したい専門家を選択してください
    2. **質問の入力**: テキストエリアに質問や相談内容を入力してください
    3. **送信**: 「回答を取得」ボタンをクリックして回答を取得してください
    
    ## 👨‍💼 利用可能な専門家
    - **データサイエンティスト**: 統計学、機械学習、データ分析に関する専門知識
    - **マーケティング戦略家**: ブランド戦略、デジタルマーケティング、市場分析に関する専門知識
    """)
    
    st.markdown("---")
    
    # メインのインターフェース
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 設定")
        
        # 専門家選択のラジオボタン
        expert_type = st.radio(
            "専門家を選択してください:",
            options=["データサイエンティスト", "マーケティング戦略家"],
            index=0
        )
        
        # 選択された専門家の説明
        expert_descriptions = {
            "データサイエンティスト": "📊 統計学、機械学習、データ分析の専門家",
            "マーケティング戦略家": "📈 ブランド戦略、デジタルマーケティングの専門家"
        }
        
        st.info(expert_descriptions[expert_type])
    
    with col2:
        st.subheader("💬 質問・相談")
        
        # 入力フォーム
        input_text = st.text_area(
            "質問や相談内容を入力してください:",
            height=150,
            placeholder="例: データ分析のプロジェクトを始めるにあたって、最初に何をすべきでしょうか？"
        )
        
        # 送信ボタン
        if st.button("🔍 回答を取得", type="primary"):
            if input_text.strip():
                with st.spinner("AIが回答を生成中..."):
                    # LLMからの回答を取得
                    response = get_llm_response(input_text, expert_type)
                
                # 回答の表示
                st.subheader("📝 回答")
                st.markdown(f"**{expert_type}からの回答:**")
                st.markdown(response)
                
            else:
                st.warning("質問内容を入力してください。")
    
    # フッター
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <small>Powered by LangChain & OpenAI GPT | Built with Streamlit</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()