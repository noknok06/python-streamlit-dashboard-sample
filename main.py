import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import sqlite3
import pandas as pd
from datetime import datetime

from manage_database import ManageDatabase as mdb
from layout import layout as l



@st.cache_data
def get_data(time1,time2):
    # SQLiteデータベースに接続

    conn = mdb('sales_database.db')

    # フィルタリング条件に基づいてデータを取得
    sql = """
        SELECT date(uri.売上日付) as date, strftime('%H', 売上時間) AS 売上時, uri.売上年, uri.売上月, toku.得意先名, sho.商品コード, cat.カテゴリー名, sho.商品名, uri.数量, CAST(sho.単価 AS INT)
        FROM 売上実績 uri INNER JOIN 得意先マスタ toku
            ON uri.得意先コード = toku.得意先コード INNER JOIN 商品マスタ sho
            ON uri.商品コード = sho.商品コード LEFT JOIN カテゴリーマスタ cat 
            ON sho.カテゴリーコード = cat.カテゴリーコード
        WHERE uri.売上日付 BETWEEN ? AND ?
        ORDER BY uri.売上日付 desc
    """
    result = conn.c.execute(sql, (time1,time2)).fetchall()

    # 接続を閉じる
    conn.disconnect_database()
    return result

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

# 年月日時の範囲を指定するスライダー
start_datetime = st.sidebar.slider("売上日時の範囲",
                        min_value=datetime(2020, 1, 1),
                        max_value=datetime(2024, 12, 31),
                        value=(datetime(2024, 1, 1), datetime(2024, 12, 31)))

# 選択された日付範囲を年月日に分割
start_year, start_month, start_day = start_datetime[
    0].year, start_datetime[0].month, start_datetime[0].day
end_year, end_month, end_day = start_datetime[1].year, start_datetime[1].month, start_datetime[1].day

result = get_data(start_datetime[0], start_datetime[1])
# メインとなるデータフレーム
df = pd.DataFrame(result)
new_columns = ['売上日付', '売上時', '売上年', '売上月', '得意先名', '商品コード', 'カテゴリー名', '商品名', '数量', '単価']
df.columns = new_columns
df['販売価格'] = df['数量'] * df['単価']

customer_selector = set(df['得意先名'])
item_selector = set(df['商品コード'])
customer_nm = st.sidebar.multiselect('得意先を選択してください', customer_selector)
item_cd = st.sidebar.multiselect('商品コードを選択してください', item_selector)

if len(customer_nm) > 0:
    df = df[df['得意先名'].isin(customer_nm)]
if len(item_cd) > 0:
    df = df[df['商品コード'].isin(item_cd)]

selling_price_total = df['販売価格'].sum()
count_total = len(df)

# col1_1, col1_2, col1_3 = st.columns(3)
col1_1, col1_2 = st.columns(2)
col1_1.metric("期間内レコード数：", f"{len(df):,}")
col1_2.metric("期間内総売上高：", f"{selling_price_total:,}")
# col1_3.metric("期間内総販売回数", f"{count_total:,}")
style_metric_cards()

col2_1, col2_2 = st.columns(2)
with col2_1:
    customer_sales_df = df.loc[:, ["得意先名","商品名","販売価格"]]
    customer_sales_df = customer_sales_df.groupby(['得意先名',"商品名"]).sum()
    customer_sales_df = customer_sales_df.reset_index()  # インデックスを列に変換
    l.toku_uri(customer_sales_df)
    
with col2_2:
    item_sales_df = df.loc[:, ["得意先名","商品名","販売価格"]]
    item_sales_df = item_sales_df.groupby(["得意先名",'商品名']).sum()
    item_sales_df = item_sales_df.reset_index()  # インデックスを列に変換
    l.item_uri(item_sales_df)

if len(customer_nm) > 0:
    sales_trends_df = df.loc[:, ["売上年","売上月","販売価格","得意先名"]]
    sales_trends_df['売上年月'] = sales_trends_df['売上年'].astype(str) + "年" + sales_trends_df['売上月'].astype(str) + "月"
    sales_trends_df = sales_trends_df.groupby(["得意先名",'売上年月']).sum()
    sales_trends_df = sales_trends_df.reset_index()  # インデックスを列に変換
    l.sales_trends(sales_trends_df)

if len(item_cd) > 0:
    item_trends_df = df.loc[:, ["売上年","売上月","販売価格","商品名"]]
    item_trends_df['売上年月'] = item_trends_df['売上年'].astype(str) + "年" + item_trends_df['売上月'].astype(str) + "月"
    item_trends_df = item_trends_df.groupby(["商品名",'売上年月']).sum()
    item_trends_df = item_trends_df.reset_index()  # インデックスを列に変換
    l.item_trends(item_trends_df)


sales_map_df = df.loc[:, ["売上時","売上月","カテゴリー名","販売価格","商品名"]]# 商品ごとに売上月別の合計と売上回数を計算する
# 商品ごとに売上月別の合計と販売回数を計算する
sales_map_df = sales_map_df.groupby(['カテゴリー名',"売上時"]).agg({'販売価格': 'sum'})

# 列名を変更する
# sales_map_df = sales_map_df.rename(columns={'販売価格': '販売価格合計'})
sales_map_df = sales_map_df.reset_index()  # インデックスを列に変換

# 必要な情報を抽出する
# sales_map_df = sales_map_df.reset_index()[['カテゴリー名', '販売価格合計']]

l.sales_map(sales_map_df)

department_group_df = df.loc[:, ["得意先名", "商品名","数量","単価", "販売価格"]]
# 「得意先名」と「商品名」でグループ化し、販売価格の合計を計算
department_group_df = department_group_df.groupby(["得意先名", "商品名"]).agg({'数量':'sum', '単価':'first', '販売価格':'sum'})
# 販売価格で降順にソート
sorted_df = department_group_df.sort_values(by='販売価格', ascending=False)
l.toku_uri_ranking(sorted_df)