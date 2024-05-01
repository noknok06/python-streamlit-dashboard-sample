import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect('sales_database.db')
c = conn.cursor()

# 商品マスタテーブルを作成
c.execute('''CREATE TABLE 商品マスタ (
                商品コード INTEGER PRIMARY KEY,
                商品名 TEXT NOT NULL,
                単価 REAL NOT NULL,
                単位 TEXT NOT NULL
            )''')

# 得意先マスタテーブルを作成
c.execute('''CREATE TABLE 得意先マスタ (
                得意先コード INTEGER PRIMARY KEY,
                得意先名 TEXT NOT NULL
            )''')

# 売上実績テーブルを作成
c.execute('''CREATE TABLE 売上実績 (
                売上年 INTEGER NOT NULL,
                売上月 INTEGER NOT NULL,
                売上日 INTEGER NOT NULL,
                売上日付 DATE NOT NULL,
                売上時間 TIME NOT NULL,
                得意先コード INTEGER NOT NULL,
                商品コード INTEGER NOT NULL,
                数量 INTEGER NOT NULL,
                FOREIGN KEY (得意先コード) REFERENCES 得意先マスタ(得意先コード),
                FOREIGN KEY (商品コード) REFERENCES 商品マスタ(商品コード)
            )''')

# 変更をコミット
conn.commit()

# 接続を閉じる
conn.close()
