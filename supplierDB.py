import sqlite3

def create_database():
    conn = sqlite3.connect('suppliers.db')
    cursor = conn.cursor()

    # 删除现有表（如果有）
    cursor.execute('DROP TABLE IF EXISTS suppliers')

    # 创建新表结构
    cursor.execute('''
    CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        wb_code TEXT,
        py_code TEXT,
        address TEXT,
        email TEXT,
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

    conn.commit()
    conn.close()

# 调用此函数以重新创建数据库
create_database()

