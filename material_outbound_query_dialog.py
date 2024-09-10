import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QHBoxLayout
)


class MaterialOutboundQueryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料出库信息")
        self.setGeometry(300, 300, 800, 400)

        layout = QVBoxLayout(self)

        # 创建出库信息表格
        self.outbound_table = QTableWidget(0, 5)  # 5列分别对应出库单号、出库时间、经办人、材料名称、数量
        self.outbound_table.setHorizontalHeaderLabels([
            "出库单号", "出库时间", "经办人", "材料名称", "数量"
        ])
        self.outbound_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.outbound_table)

        # 添加“刷新”按钮
        button_layout = QHBoxLayout()
        refresh_button = QPushButton("刷新")
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)

        # 绑定按钮的信号与槽
        refresh_button.clicked.connect(self.load_outbound_data)

        # 初始化加载出库数据
        self.load_outbound_data()

    def load_outbound_data(self):
        """从数据库加载材料出库信息"""
        # 清空表格中的现有内容
        self.outbound_table.setRowCount(0)

        # 连接到SQLite数据库
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        # 查询 material_outbound 表中的所有出库数据
        cursor.execute('''
            SELECT outbound_number, outbound_date, handler, material_name, quantity
            FROM material_outbound
        ''')
        outbound_records = cursor.fetchall()
        conn.close()

        # 将每一条出库记录插入表格中
        for row_number, record in enumerate(outbound_records):
            self.outbound_table.insertRow(row_number)
            for column_number, data in enumerate(record):
                self.outbound_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
