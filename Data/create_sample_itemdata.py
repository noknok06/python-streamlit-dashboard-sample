import sqlite3

# SQLite3データベースに接続
conn = sqlite3.connect('sales_database.db')
cursor = conn.cursor()

# 商品マスタにサンプル商品を30品登録するSQLクエリ
sql_query = """
INSERT INTO 商品マスタ (商品コード, 商品名, 単価, 単位) VALUES
('001', '商品A', 100, '個'),
('002', '商品B', 200, '個'),
('003', '商品C', 150, '個'),
('004', '商品D', 120, '個'),
('005', '商品E', 180, '個'),
('006', '商品F', 90, '個'),
('007', '商品G', 250, '個'),
('008', '商品H', 300, '個'),
('009', '商品I', 80, '個'),
('010', '商品J', 160, '個'),
('011', '商品K', 220, '個'),
('012', '商品L', 130, '個'),
('013', '商品M', 170, '個'),
('014', '商品N', 110, '個'),
('015', '商品O', 140, '個'),
('016', '商品P', 190, '個'),
('017', '商品Q', 270, '個'),
('018', '商品R', 320, '個'),
('019', '商品S', 70, '個'),
('020', '商品T', 230, '個'),
('021', '商品U', 260, '個'),
('022', '商品V', 210, '個'),
('023', '商品W', 340, '個'),
('024', '商品X', 150, '個'),
('025', '商品Y', 200, '個'),
('026', '商品Z', 280, '個'),
('027', '商品AA', 330, '個'),
('028', '商品AB', 240, '個'),
('029', '商品AC', 290, '個'),
('030', '商品AD', 310, '個');
"""

# SQLクエリを実行
cursor.execute(sql_query)

# 変更をコミット
conn.commit()

# 接続を閉じる
conn.close()
