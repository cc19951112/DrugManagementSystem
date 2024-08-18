import sqlite3
import pandas as pd

def create_database_from_excel(excel_file):
    # 读取Excel文件中的供应商数据
    df = pd.read_excel(excel_file, sheet_name=0, usecols="B:N", skiprows=4, dtype={
        'SH': str,   # 税号
        'YZBM': str, # 邮政编码
        'ZH': str,    # 账号
        'BM': str   #编码
    })

    # 重命名DataFrame列以匹配数据库表结构
    df.columns = ['bm', 'name', 'wb_code', 'py_code', 'address', 'postal_code', 'fax', 'phone', 'contact', 'bank', 'tax', 'account', 'note']

    # 连接到SQLite数据库
    conn = sqlite3.connect('suppliers.db')
    cursor = conn.cursor()

    # 删除现有表（如果有）
    cursor.execute('DROP TABLE IF EXISTS suppliers')

    # 创建新表结构
    cursor.execute('''
    CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bm TEXT NOT NULL,
        name TEXT NOT NULL,
        wb_code TEXT,
        py_code TEXT,
        address TEXT,
        postal_code TEXT,
        fax TEXT,
        phone TEXT,
        contact TEXT,
        bank TEXT,
        account TEXT,
        tax TEXT,
        note TEXT,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES suppliers (id)
    )
    ''')

    # 创建字典来存储编码与数据库ID的映射
    bm_to_id = {}

    # 插入数据到数据库
    for index, row in df.iterrows():
        bm = row['bm']
        parent_id = None

        # 判断编码的层级关系
        if len(bm) == 6:  # 二级编码
            parent_bm = bm[:3]  # 找到一级编码
            parent_id = bm_to_id.get(parent_bm)
        elif len(bm) == 9:  # 三级编码
            parent_bm = bm[:6]  # 找到二级编码
            parent_id = bm_to_id.get(parent_bm)

        cursor.execute('''
        INSERT INTO suppliers (bm, name, wb_code, py_code, address, postal_code, fax, phone, contact, bank, account, tax, note, parent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', 
        (bm, row['name'], row['wb_code'], row['py_code'], row['address'], row['postal_code'], row['fax'], row['phone'], row['contact'], row['bank'], row['account'], row['tax'], row['note'], parent_id))

        # 获取插入记录的ID并更新bm_to_id映射
        inserted_id = cursor.lastrowid
        bm_to_id[bm] = inserted_id

    # 提交事务并关闭数据库连接
    conn.commit()
    conn.close()

# 调用此函数以根据Excel文件重新创建数据库
create_database_from_excel('suppliers.xls')
