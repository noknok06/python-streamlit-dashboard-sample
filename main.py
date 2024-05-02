import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import sqlite3
import pandas as pd
from datetime import datetime

from manage_database import ManageDatabase as mdb
from layout import layout as l


st.set_page_config(
    page_title="sample-app",
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

conn = mdb('sales_database.db')

# 年月日時の範囲を指定するスライダー
start_datetime = st.sidebar.slider("売上日時の範囲",
                        min_value=datetime(2020, 1, 1),
                        max_value=datetime(2024, 12, 31),
                        value=(datetime(2024, 1, 1), datetime(2024, 12, 31)))

# 選択された日付範囲を年月日に分割
start_year, start_month, start_day = start_datetime[
    0].year, start_datetime[0].month, start_datetime[0].day
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
result = conn.c.execute(sql, (start_datetime[0], start_datetime[1])).fetchall()

# 接続を閉じる
conn.disconnect_database()

# メインとなるデータフレーム
df = pd.DataFrame(result)
new_columns = ['売上日付', '得意先名', '商品名', '数量', '単価']
df.columns = new_columns
df['販売価格'] = df['数量'] * df['単価']

tokui_nm = st.sidebar.text_input('得意先名を入力してください')

if tokui_nm != "":
    df = df[df['得意先名'].str.contains(tokui_nm)]

hanbai_total = df['販売価格'].sum()
count_total = len(df)

col1, col2 = st.columns(2)
col1.metric("期間内総売上高：", f"{hanbai_total:,}")
col2.metric("期間内総販売回数", f"{count_total:,}")
style_metric_cards()

with col1:
    toku_uri_df = df
    toku_uri_df = df.loc[:, ["得意先名","販売価格"]]
    toku_uri_df = toku_uri_df.groupby(['得意先名']).sum()
    toku_uri_df = toku_uri_df.reset_index()  # インデックスを列に変換
    l.toku_uri(toku_uri_df)
    
with col2:
    item_uri_df = df
    item_uri_df = df.loc[:, ["商品名","販売価格"]]
    item_uri_df = item_uri_df.groupby(['商品名']).sum()
    item_uri_df = item_uri_df.reset_index()  # インデックスを列に変換
    l.item_uri(item_uri_df)

department_group_df = df.loc[:, ["得意先名", "商品名","数量","単価", "販売価格"]]
department_group_df = department_group_df.groupby(["得意先名", "商品名"]).sum()
sorted_df = department_group_df.sort_values(by='販売価格', ascending=False)
l.toku_uri_ranking(sorted_df)