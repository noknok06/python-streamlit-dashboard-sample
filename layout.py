import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

class layout:

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    # 得意先商品売上 TOP10
    def toku_uri_ranking(df):
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.subheader("得意先商品売上 TOP10")
        with col1_2:
            on_click = st.button("Reset", key="reset_button", type="primary")
        
        if on_click == True:
            text_input = st.text_input(
                "ランキング表示数",
                "10",
                key="placeholder",
            )
            text_input = 10
        else:
            text_input = st.text_input(
                "ランキング表示数",
                "10",
                key="placeholder",
            )

        st.table(df.head(int(text_input)))
        
        csv = layout.convert_df(df.head(int(text_input)))
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='large_df.csv',
            mime='text/csv',
        )   

    def toku_uri(df):
        st.subheader("得意先別売上")
        # Plotlyのfigを作成
        fig = px.bar(df, x='得意先名', y='販売価格')
        # Streamlitに表示
        st.plotly_chart(fig, use_container_width=True)

    def item_uri(df):
        st.subheader("商品別売上")
        # Plotlyのfigを作成
        fig = px.bar(df, x='商品名', y='販売価格')
        # Streamlitに表示
        st.plotly_chart(fig, use_container_width=True)