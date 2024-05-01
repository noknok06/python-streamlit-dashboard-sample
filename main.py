import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# SQLiteデータベースに接続
conn = sqlite3.connect('sales_database.db')
c = conn.cursor()

# 売上実績データを取得する関数
def get_sales_data(sql):
    c.execute(sql)
    rows = c.fetchall()
    columns = [desc[0] for desc in c.description]
    return pd.DataFrame(rows, columns=columns)

# 売上実績チャートを作成する関数
def plot_sales_chart():
    df = get_sales_data()
    if df.empty:
        st.warning("売上実績データがありません。")
    else:
        st.write("## 売上実績チャート")
        sales_chart_data = df.groupby('売上日').sum()['数量']
        sales_chart_data.plot(kind='line', figsize=(10, 6))
        plt.xlabel('売上日')
        plt.ylabel('数量')
        plt.title('売上実績')
        st.pyplot()

# 年月日時の範囲を指定するスライダー
start_datetime = st.slider("売上日時の範囲", 
                           min_value=datetime(2020, 1, 1), 
                           max_value=datetime(2024, 12, 31),
                           value=(datetime(2024, 1, 1), datetime(2024, 12, 31)))

# 選択された日付範囲を年月日に分割
start_year, start_month, start_day = start_datetime[0].year, start_datetime[0].month, start_datetime[0].day
end_year, end_month, end_day = start_datetime[1].year, start_datetime[1].month, start_datetime[1].day

# フィルタリング条件に基づいてデータを取得
sql = """
    SELECT uri.売上日付, toku.得意先名, sho.商品名, uri.数量, CAST(sho.単価 AS INT)
    FROM 売上実績 uri INNER JOIN 得意先マスタ toku
        ON uri.得意先コード = toku.得意先コード INNER JOIN 商品マスタ sho
        ON uri.商品コード = sho.商品コード
    WHERE uri.売上日付 BETWEEN ? AND ?
    ORDER BY uri.売上日付 desc
"""
result = c.execute(sql, (start_datetime[0], start_datetime[1])).fetchall()

# 接続を閉じる
conn.close()

# メインとなるデータフレーム
df = pd.DataFrame(result)
new_columns = ['売上日付', '得意先名', '商品名', '数量', '単価']
df.columns = new_columns

tokui_nm = st.text_input('得意先名を入力してください')

if tokui_nm != "":
    df = df[df['得意先名'].str.contains(tokui_nm)]

total = df['単価'].sum()

st.text("総売上高：" + str(int(total)))

col1, col2 = st.columns(2)

with col1:
    st.subheader("得意先商品売上 TOP10")
    new_columns = ['売上日付', '得意先名', '商品名', '数量', '単価']
    df.columns = new_columns
    department_group_df = df.drop(['売上日付'], axis=1)
    department_group_df = department_group_df.groupby(["得意先名", "商品名"]).sum()
    sorted_df = department_group_df.sort_values(by='単価', ascending=False)
    st.table(sorted_df.head(10))

with col2:
    st.subheader("商品別売上")
    toku_uri_df = df
    toku_uri_df = df.drop(['売上日付', '得意先名', '数量'], axis=1)
    toku_uri_df = toku_uri_df.groupby(['商品名']).sum()
    toku_uri_df = toku_uri_df.reset_index()  # インデックスを列に変換
    new_columns = ['商品名', '単価']
    toku_uri_df.columns = new_columns
    # Plotlyのfigを作成
    fig = px.bar(toku_uri_df, x='商品名', y='単価')
    # Streamlitに表示
    st.plotly_chart(fig, use_container_width=True)
