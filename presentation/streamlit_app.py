import sys
import os

# プロジェクトのルートディレクトリをパスに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import streamlit as st
from application.ad_recommender_service import AdRecommenderService

# ページ設定
st.set_page_config(layout="wide")

# CSSファイルの読み込みと適用
def load_css(file_name):
    with open(os.path.join(os.path.dirname(__file__), 'styles', file_name)) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# CSSの適用
load_css('main.css')

# セッション状態の初期化
if 'llm_output' not in st.session_state:
    st.session_state.llm_output = ""

# デフォルトの商品情報テンプレート
default_product_info = """商品名 : 

商品ジャンル(3階層) : 

価格 : 

割引後の価格 : 

割引率 :
"""

def main():
    st.markdown("""
    <style>
    div[class^="block-container"] {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    st.title('楽天広告枠アドバイザー')

    recommender_service = AdRecommenderService()
    
    ad_spaces_file = 'infrastructure/広告枠一覧 - 広告枠.csv'
    past_recommendations_file = 'infrastructure/広告枠一覧 - 広告枠、商品、理由.csv'

    # タブの作成
    tab1, tab2, tab3, tab4 = st.tabs(["メイン", "プロンプト", "広告枠一覧", "枠の選択例"])

    with tab1:
        # メインの機能
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("商品情報入力")
            user_input = st.text_area("商品情報を入力してください：", value=default_product_info, height=400)
            
            if st.button('おすすめの広告枠を取得'):
                if user_input.strip() != default_product_info.strip():
                    with st.spinner('分析中...'):
                        recommendations = recommender_service.get_recommendations(user_input, ad_spaces_file, past_recommendations_file)
                    st.session_state.llm_output = recommendations
                else:
                    st.warning('商品情報を入力してください。')

        with col2:
            st.header("レコメンデーション結果")
            st.text_area(
                "LLMのアウトプット",
                value=st.session_state.llm_output,
                height=400,
                key="llm_output_display"
            )

    with tab2:
        st.header("プロンプト編集")
        current_prompt = recommender_service.get_prompt_template()
        new_prompt = st.text_area("プロンプトテンプレート", value=current_prompt, height=400)
        if st.button('プロンプトを更新'):
            recommender_service.update_prompt_template(new_prompt)
            st.success('プロンプトが更新されました。')

    with tab3:
        st.header("広告枠一覧")
        ad_spaces_df = recommender_service.get_ad_spaces_dataframe(ad_spaces_file)
        edited_ad_spaces = st.data_editor(ad_spaces_df, num_rows="dynamic")
        if st.button('広告枠一覧を保存'):
            recommender_service.save_ad_spaces_dataframe(edited_ad_spaces, ad_spaces_file)
            st.success('広告枠一覧が保存されました。')

    with tab4:
        st.header("枠の選択例")
        past_recommendations_df = recommender_service.get_past_recommendations_dataframe(past_recommendations_file)
        edited_past_recommendations = st.data_editor(past_recommendations_df, num_rows="dynamic")
        if st.button('枠の選択例を保存'):
            recommender_service.save_past_recommendations_dataframe(edited_past_recommendations, past_recommendations_file)
            st.success('枠の選択例が保存されました。')

if __name__ == "__main__":
    main()