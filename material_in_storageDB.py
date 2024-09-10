import sqlite3

# 连接到SQLite数据库（如果数据库不存在将会创建一个新的数据库）
conn = sqlite3.connect('material.db')

# 创建一个游标对象，用于执行SQL语句
cursor = conn.cursor()

# 创建材料入库记录表的SQL语句
create_table_sql = '''
CREATE TABLE IF NOT EXISTS material_storage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    storage_number TEXT NOT NULL,
    storage_date DATE NOT NULL,
    handler TEXT NOT NULL,
    material_name TEXT NOT NULL,
    supplier TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    purchase_price REAL NOT NULL
);
'''

# 执行创建表的SQL语句
cursor.execute(create_table_sql)

# 提交事务
conn.commit()

# 关闭连接
conn.close()

print("材料入库记录表创建成功！")
