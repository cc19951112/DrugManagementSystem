import sqlite3
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class InventoryQueryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("药品库存查询")
        self.setGeometry(200, 200, 1024, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 创建表格
        self.table_widget = QTableWidget(0, 20)  # 设置列数为20
        self.table_widget.setHorizontalHeaderLabels([
            "序号", "药品编码", "药品名称", "规格", "产地", "批次", "生产批号",
            "单位", "库存", "药品售价", "售价金额", "药品进价", "进价金额", 
            "毛利", "毛利率", "失效日期", "使用期限", "国家医保代码", 
            "国家医保名称", "供应商"
        ])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setShowGrid(True)  # 显示网格线

        # 将表格加入到布局中
        layout.addWidget(self.table_widget)

        #此处你可以通过调用数据库填充表格内容（如果需要）
        self.load_data()

    #你可以定义一个方法来从数据库加载数据到表格
    def load_data(self):
        # 连接数据库并查询库存数据
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory')
        inventory_data = cursor.fetchall()
    
        # 填充表格
        for row_data in inventory_data:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.table_widget.setItem(row_position, column, QTableWidgetItem(str(data)))
    
        conn.close()

