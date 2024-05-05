import sqlite3
import random
from datetime import datetime, timedelta

# 商品カテゴリーごとの売り上げピークの時間帯の設定
category_peak_times = {
    1: (7, 8),    # 昼食時がピーク
    2: (14, 14),  # 夕食後がピーク
    3: (15, 15),  # 夜間がピーク
    4: (17, 17),  # 夜間がピーク
    5: (7, 7),    # 夜間がピーク
    6: (21, 21),  # 夜間がピーク
    7: (12, 13),  # 夜間がピーク
    8: (16, 16),  # 夜間がピーク
    9: (21, 21),  # 夜間がピーク
    10: (21, 21), # 夜間がピーク
    # 他のカテゴリーについても同様に設定
}

# SQLite3データベースに接続
conn = sqlite3.connect('sales_database.db')
cursor = conn.cursor()

# 商品マスタから商品コードとカテゴリー名のリストを取得
cursor.execute("SELECT 商品コード, カテゴリーコード FROM 商品マスタ")
product_categories = {row[0]: row[1] for row in cursor.fetchall()}

# 得意先マスタから得意先コードのリストを取得
cursor.execute("SELECT 得意先コード FROM 得意先マスタ")
customer_codes = [row[0] for row in cursor.fetchall()]

# 売上実績のデータを作成して登録
for _ in range(50000):
    # ランダムな得意先コードと商品コードを選択
    customer_code = random.choice(customer_codes)
    product_code = random.choice(list(product_categories.keys()))
    
    # 商品のカテゴリー名からピークの時間帯を取得
    category_name = product_categories[product_code]
    peak_start, peak_end = category_peak_times.get(category_name, (9, 22))  # デフォルトは午前9時から午後10時
    
    # ランダムな売上日時を生成（ピークの時間帯に偏る）
    sales_date = datetime.now() - timedelta(days=random.randint(0, 1826))
    sales_date = sales_date.replace(hour=random.randint(peak_start, peak_end), minute=random.randint(0, 59), second=random.randint(0, 59))
    sales_year = sales_date.year
    sales_month = sales_date.month
    sales_day = sales_date.day
    sales_time = sales_date.strftime("%H:%M:%S")
    
    # ランダムな数量を生成
    quantity = random.randint(1, 100)
    
    # 売上実績をデータベースに登録
    cursor.execute("INSERT INTO 売上実績 (売上年, 売上月, 売上日, 売上日付, 売上時間, 得意先コード, 商品コード, 数量) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (sales_year, sales_month, sales_day, sales_date, sales_time, customer_code, product_code, quantity))

# 変更をコミット
conn.commit()

# 接続を閉じる
conn.close()

print("finish")
