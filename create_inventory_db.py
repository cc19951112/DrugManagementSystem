import sqlite3

def create_inventory_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # 删除现有表（如果有）
    cursor.execute('DROP TABLE IF EXISTS inventory')

    # 创建新的库存表结构
    cursor.execute('''
    CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug_code TEXT NOT NULL,
        drug_name TEXT NOT NULL,
        specification TEXT,
        origin TEXT,
        batch_number TEXT,
        production_batch TEXT,
        unit TEXT,
        stock REAL,
        drug_sale_price REAL,
        sale_amount REAL,
        drug_purchase_price REAL,
        purchase_amount REAL,
        gross_profit REAL,
        gross_profit_rate REAL,
        expiration_date TEXT,
        usage_period TEXT,
        insurance_code TEXT,
        insurance_name TEXT,
        supplier TEXT
    )
    ''')

    # 插入一些示例数据
    sample_data = [
        ("2024001", "药品A", "100mg", "产地A", "12345", "A1001", "瓶", 50, 10.0, 500.0, 8.0, 400.0, 100.0, "25.0%", "2025-12-31", "2年", "IC001", "医保A", "供应商A"),
        ("2024002", "药品B", "200mg", "产地B", "12346", "A1002", "盒", 100, 20.0, 2000.0, 16.0, 1600.0, 400.0, "20.0%", "2024-11-30", "1年", "IC002", "医保B", "供应商B"),
        ("2024003", "药品C", "150mg", "产地C", "12347", "A1003", "片", 200, 15.0, 3000.0, 12.0, 2400.0, 600.0, "20.0%", "2026-10-15", "3年", "IC003", "医保C", "供应商C")
        # 你可以继续添加更多示例数据...
    ]

    cursor.executemany('''
    INSERT INTO inventory (drug_code, drug_name, specification, origin, batch_number, production_batch, unit, stock, drug_sale_price, sale_amount, drug_purchase_price, purchase_amount, gross_profit, gross_profit_rate, expiration_date, usage_period, insurance_code, insurance_name, supplier)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_inventory_database()
