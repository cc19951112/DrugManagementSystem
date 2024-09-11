import sqlite3

# 连接到SQLite数据库，如果数据库不存在将会创建一个新的数据库
conn = sqlite3.connect('material.db')

# 创建一个游标对象，用于执行SQL语句
cursor = conn.cursor()

# 创建材料表的SQL语句，增加新要求的字段
create_table_sql = '''
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    spec TEXT NOT NULL,               -- 新增：规格
    origin TEXT NOT NULL,             -- 新增：产地
    manufacturer TEXT NOT NULL,       -- 新增：生产厂家
    packaging_unit TEXT NOT NULL,     -- 新增：包装单位
    packaging_price REAL NOT NULL,
    expiration_date DATE NOT NULL,
    inventory_count INTEGER DEFAULT 0
);
'''

# 执行创建表的SQL语句
cursor.execute(create_table_sql)

# 插入十条材料信息的SQL语句，包含新增的字段
insert_materials_sql = '''
INSERT INTO materials (code, name, spec, origin, manufacturer, packaging_unit, packaging_price, expiration_date, inventory_count)
VALUES 
    ('M001', '感冒药', '10片', '中国', '制药厂A', '盒', 15.5, '2025-12-31', 0),
    ('M002', '止痛药', '20片', '美国', '制药厂B', '盒', 20.0, '2024-08-15', 0),
    ('M003', '维生素C', '100片', '德国', '制药厂C', '瓶', 12.0, '2026-05-10', 0),
    ('M004', '抗生素', '10瓶', '法国', '制药厂D', '瓶', 45.0, '2023-11-20', 0),
    ('M005', '抗过敏药', '15片', '日本', '制药厂E', '盒', 18.0, '2025-03-01', 0),
    ('M006', '消炎药', '30片', '印度', '制药厂F', '瓶', 25.0, '2024-06-30', 0),
    ('M007', '胃药', '10袋', '中国', '制药厂G', '袋', 30.0, '2025-10-15', 0),
    ('M008', '降压药', '10片', '美国', '制药厂H', '盒', 35.0, '2026-02-28', 0),
    ('M009', '止咳药', '250ml', '德国', '制药厂I', '瓶', 22.0, '2024-09-05', 0),
    ('M010', '镇静药', '10片', '中国', '制药厂J', '盒', 40.0, '2023-12-25', 0);
'''

# 执行插入数据的SQL语句
cursor.execute(insert_materials_sql)

# 提交事务
conn.commit()

# 关闭连接
conn.close()

print("材料信息已成功插入到数据库material.db中！")


import sqlite3

# 连接到SQLite数据库（如果数据库不存在将会创建一个新的数据库）
conn = sqlite3.connect('material.db')

# 创建一个游标对象，用于执行SQL语句
cursor = conn.cursor()

# 创建材料入库记录表的SQL语句，新增生产批号、生产日期、失效日期、进价、售价
create_table_sql = '''
CREATE TABLE IF NOT EXISTS material_storage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    storage_number TEXT NOT NULL,
    storage_date DATE NOT NULL,
    handler TEXT NOT NULL,
    material_name TEXT NOT NULL,
    supplier TEXT NOT NULL,
    batch_number TEXT NOT NULL,         -- 新增：生产批号
    production_date DATE NOT NULL,      -- 新增：生产日期
    expiration_date DATE NOT NULL,      -- 新增：失效日期
    purchase_price REAL NOT NULL,       -- 新增：进价
    selling_price REAL NOT NULL,        -- 新增：售价
    quantity INTEGER NOT NULL
);
'''

# 执行创建表的SQL语句
cursor.execute(create_table_sql)

# 提交事务
conn.commit()

# 关闭连接
conn.close()

print("材料入库记录表创建成功！")

import sqlite3

# 连接到SQLite数据库（如果数据库不存在将会创建一个新的数据库）
conn = sqlite3.connect('material.db')

# 创建一个游标对象，用于执行SQL语句
cursor = conn.cursor()

# 创建材料出库记录表的SQL语句，增加调拨科室，并读取批号、失效日期、售价
create_table_sql = '''
CREATE TABLE IF NOT EXISTS material_outbound (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    outbound_number TEXT NOT NULL,
    outbound_date DATE NOT NULL,
    handler TEXT NOT NULL,
    material_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    department TEXT NOT NULL,           -- 新增：调拨科室
    batch_number TEXT,                  -- 新增：批号（只读）
    expiration_date DATE,               -- 新增：失效日期（只读）
    selling_price REAL                  -- 新增：售价（只读）
);
'''

# 执行创建表的SQL语句
cursor.execute(create_table_sql)

# 提交事务
conn.commit()

# 关闭连接
conn.close()

print("材料出库记录表创建成功！")
