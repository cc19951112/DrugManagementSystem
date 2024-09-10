import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QHBoxLayout
)


class MaterialStorageQueryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料入库信息")
        self.setGeometry(300, 300, 900, 400)

        layout = QVBoxLayout(self)

        # 创建入库信息表格
        self.storage_table = QTableWidget(0, 7)  # 7列分别对应入库单号、入库时间、经办人、材料名称、供应商、数量、进价
        self.storage_table.setHorizontalHeaderLabels([
            "入库单号", "入库时间", "经办人", "材料名称", "供应商", "数量", "材料进价"
        ])
        self.storage_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.storage_table)

        # 添加“刷新”按钮
        button_layout = QHBoxLayout()
        refresh_button = QPushButton("刷新")
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)

        # 绑定按钮的信号与槽
        refresh_button.clicked.connect(self.load_storage_data)

        # 初始化加载入库数据
        self.load_storage_data()

    def load_storage_data(self):
        """从数据库加载材料入库信息"""
        # 清空表格中的现有内容
        self.storage_table.setRowCount(0)

        # 连接到SQLite数据库
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        # 查询 material_storage 表中的所有入库数据
        cursor.execute('''
            SELECT storage_number, storage_date, handler, material_name, supplier, quantity, purchase_price 
            FROM material_storage
        ''')
        storage_records = cursor.fetchall()
        conn.close()

        # 将每一条入库记录插入表格中
        for row_number, record in enumerate(storage_records):
            self.storage_table.insertRow(row_number)
            for column_number, data in enumerate(record):
                self.storage_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


