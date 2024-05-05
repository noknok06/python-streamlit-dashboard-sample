import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd

class layout:

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    # 得意先商品売上 TOP10
    def toku_uri_ranking(df):
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.subheader("得意先商品売上 Ranking")
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
        # 商品ごとに異なる色を指定するためのカラーマップを作成
        unique_products = df['商品名'].unique()
        color_map = {product: unique_products[i] for i, product in enumerate(unique_products)}

        # チャートデータを作成
        chart_data = pd.DataFrame({
            "得意先": df['得意先名'],
            "売上": df['販売価格'],
            "商品": df['商品名'].map(color_map),  # 商品ごとの色情報
        })

        fig = px.bar(chart_data, x="得意先", y="売上", color="商品")

        # グラフを表示
        st.plotly_chart(fig, use_container_width=True)

    def item_uri(df):
        st.subheader("商品別売上")
        unique_products = df['得意先名'].unique()
        color_map = {product: unique_products[i] for i, product in enumerate(unique_products)}
        # チャートデータを作成
        chart_data = pd.DataFrame({
            "商品": df['商品名'],
            "売上": df['販売価格'],
            "得意先": df['得意先名'].map(color_map),  # 商品ごとの色情報
        })

        fig = px.bar(chart_data, x="商品", y="売上", color="得意先")

        # グラフを表示
        st.plotly_chart(fig, use_container_width=True)

    def sales_trends(df):
        st.subheader("得意先売上推移")
        unique_products = df['得意先名'].unique()
        color_map = {product: unique_products[i] for i, product in enumerate(unique_products)}
        chart_data = pd.DataFrame(
        {
            "売上年月": df['売上年月'],
            "販売価格": df['販売価格'],
            "得意先名": df['得意先名'].map(color_map),  # 得意先ごとの色情報
        }
        )

        st.line_chart(chart_data, x="売上年月", y="販売価格", color="得意先名")

    def item_trends(df):
        st.subheader("商品売上推移")
        unique_products = df['商品名'].unique()
        color_map = {product: unique_products[i] for i, product in enumerate(unique_products)}
        chart_data = pd.DataFrame(
        {
            "売上年月": df['売上年月'],
            "販売価格": df['販売価格'],
            "商品名": df['商品名'].map(color_map),  # 商品ごとの色情報
        }
        )

        st.line_chart(chart_data, x="売上年月", y="販売価格", color="商品名")

    def sales_map(df):

        st.subheader("売上時間帯マップ")
        unique_products = df['カテゴリー名'].unique()
        color_map = {product: unique_products[i] for i, product in enumerate(unique_products)}

        chart_data = pd.DataFrame(
        {
            "販売価格合計": df['販売価格'],
            "売上時間帯": df['売上時'],
            "カテゴリー名": df['カテゴリー名'],
            "カテゴリー色": df['カテゴリー名'].map(color_map),  # 得意先ごとの色情報
        }
        )

        st.scatter_chart(
            chart_data,
            x='売上時間帯',
            y='カテゴリー名',
            size="販売価格合計",
            color='カテゴリー名',  # Optional
        )