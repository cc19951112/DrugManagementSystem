import sqlite3
import pandas as pd

def create_materials_database_from_excel(excel_file):
    # 读取Excel文件中的材料数据
    df = pd.read_excel(excel_file, sheet_name=0, usecols="B:R", skiprows=5)

    # 使用一次分割获取“产地”，剩下的作为“名称和规格”
    df[['名称和规格', '产地']] = df['名称 /  规格 / 产地'].str.rsplit('/', 1, expand=True)
    
    # 然后从“名称和规格”中再进行分割，获取“名称”和“规格”
    df[['名称', '规格']] = df['名称和规格'].str.split('/', 1, expand=True)

    # 连接到SQLite数据库
    conn = sqlite3.connect('materials.db')
    cursor = conn.cursor()

    # 删除现有表（如果有）
    cursor.execute('DROP TABLE IF EXISTS material_categories')
    cursor.execute('DROP TABLE IF EXISTS material_attributes')
    cursor.execute('DROP TABLE IF EXISTS materials')

    # 创建材料分类表结构
    cursor.execute('''
    CREATE TABLE material_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES material_categories (id)
    )
    ''')

    # 创建材料属性表结构
    cursor.execute('''
    CREATE TABLE material_attributes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        name TEXT NOT NULL
    )
    ''')
    
    # 创建材料表结构
    cursor.execute('''
    CREATE TABLE materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        code TEXT,
        name TEXT,
        spec TEXT,
        origin TEXT,
        attribute TEXT,
        cost REAL,
        pinyin TEXT,
        wb_code TEXT,
        package_unit TEXT,
        use_unit TEXT,
        package_conversion REAL,
        package_price REAL,
        use_price REAL,
        package_sale REAL,
        use_sale REAL,
        manufacturer TEXT
    )
    ''')

    # 插入材料数据
    for index, row in df.iterrows():
        cursor.execute('''
        INSERT INTO materials (
            category, code, name, spec, origin, attribute, cost, pinyin, wb_code, 
            package_unit, use_unit, package_conversion, package_price, use_price, 
            package_sale, use_sale, manufacturer
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['分类'], row['编码'], row['名称'], row['规格'], row['产地'], 
            row['属性'], row['费用'], row['拼音码'], row['五笔码'], 
            row['包装单位'], row['使用单位'], row['包装换算'], 
            row['包装批价'], row['使用批价'], row['包装售价'], 
            row['使用售价'], row['生产厂家']
        ))

    # 定义材料分类数据
    categories = [
        "一般材料",
        "一次性材料",
        # "消毒片",
        # "专科材料",
        # "紫外线灯",
        # "漂白粉",
        # "消毒类",
        # "消毒药水",
        # "麻醉药品",
        # "化证材料",
        "办公耗材",
        "检验科类"
        # "妇科类",
        # "C14科",
        # "胶囊胃肠镜",
        # "耳鼻喉科",
        # "口腔科"
    ]

    # 插入材料分类数据
    for category in categories:
        cursor.execute('''
        INSERT INTO material_categories (name, parent_id)
        VALUES (?, NULL)''', (category,))

    # 定义材料属性数据
    attributes = [
        ("01", "一次性输液类"),
        ("02", "一次性敷料类"),
        ("03", "一次性器械类"),
        ("04", "可重复使用器械类"),
        ("05", "消毒灭菌类"),
        ("06", "一次性耗材类"),
        ("07", "化试"),
        ("08", "针灸类"),
        ("09", "麻醉类"),
        ("10", "其它类"),
        ("11", "办公用品类"),
        ("12", "检验科类"),
        ("13", "妇科类"),
        ("14", "口腔科")
    ]

    # 插入材料属性数据
    for code, name in attributes:
        cursor.execute('''
        INSERT INTO material_attributes (code, name)
        VALUES (?, ?)''', (code, name))

    conn.commit()
    conn.close()

# 调用此函数以根据Excel文件重新创建数据库
create_materials_database_from_excel('material.xls')
