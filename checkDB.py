import sqlite3

def check_table_structure():
    conn = sqlite3.connect('suppliers.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(suppliers);")
    columns = cursor.fetchall()

    for column in columns:
        print(f"Column ID: {column[0]}, Name: {column[1]}, Type: {column[2]}")
    
    conn.close()

check_table_structure()
