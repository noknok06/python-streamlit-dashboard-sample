import sqlite3
import random
from datetime import datetime, timedelta

# SQLite3データベースに接続
conn = sqlite3.connect('sales_database.db')
cursor = conn.cursor()

# 商品マスタから商品コードのリストを取得
cursor.execute("SELECT 商品コード FROM 商品マスタ")
product_codes = [row[0] for row in cursor.fetchall()]

# 得意先マスタから得意先コードのリストを取得
cursor.execute("SELECT 得意先コード FROM 得意先マスタ")
customer_codes = [row[0] for row in cursor.fetchall()]

# 売上実績のデータを作成して登録
for _ in range(500000):
    # ランダムな売上日時を生成
    sales_date = datetime.now() - timedelta(days=random.randint(0, 1826))
    sales_year = sales_date.year
    sales_month = sales_date.month
    sales_day = sales_date.day
    sales_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
    
    # ランダムな得意先コードと商品コードを選択
    customer_code = random.choice(customer_codes)
    product_code = random.choice(product_codes)
    
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
