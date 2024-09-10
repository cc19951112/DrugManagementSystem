import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QHBoxLayout
)


class InventoryQueryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料库存信息")
        self.setGeometry(300, 300, 800, 400)

        layout = QVBoxLayout(self)

        # 创建库存信息表格
        self.inventory_table = QTableWidget(0, 5)  # 5列分别对应编码、名称、包装价格、失效日期、库存数量
        self.inventory_table.setHorizontalHeaderLabels([
            "编码", "材料名称", "包装价格", "失效日期", "库存数量"
        ])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.inventory_table)

        # 添加“刷新”按钮
        button_layout = QHBoxLayout()
        refresh_button = QPushButton("刷新")
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)

        # 绑定按钮的信号与槽
        refresh_button.clicked.connect(self.load_inventory_data)

        # 初始化加载库存数据
        self.load_inventory_data()

    def load_inventory_data(self):
        """从数据库加载材料库存信息"""
        # 清空表格中的现有内容
        self.inventory_table.setRowCount(0)

        # 连接到SQLite数据库
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        # 查询 materials 表中的所有库存数据
        cursor.execute('SELECT code, name, packaging_price, expiration_date, inventory_count FROM materials')
        materials = cursor.fetchall()
        conn.close()

        # 将每一条库存信息插入表格中
        for row_number, material in enumerate(materials):
            self.inventory_table.insertRow(row_number)
            for column_number, data in enumerate(material):
                self.inventory_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

