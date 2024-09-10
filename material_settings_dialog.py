import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QHBoxLayout, QDialog, QLabel, 
    QLineEdit, QMessageBox, QDateEdit, QGridLayout
)
from PyQt5.QtCore import Qt, QDate


class MaterialSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 材料详细信息表格
        self.material_table = QTableWidget(0, 4)  # 设置列数为4，分别是编码、名称、包装价格、失效日期
        self.material_table.setHorizontalHeaderLabels([
            "编码", "名称", "包装价格", "失效日期"
        ])
        self.material_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.material_table)

        # 添加底部按钮布局
        button_layout = QHBoxLayout()
        add_button = QPushButton("增加")
        edit_button = QPushButton("修改")
        delete_button = QPushButton("删除")

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        main_layout.addLayout(button_layout)

        # 绑定按钮到相应的操作函数
        add_button.clicked.connect(self.add_material)
        edit_button.clicked.connect(self.edit_material)
        delete_button.clicked.connect(self.delete_material)

        # 初始化加载材料数据
        self.load_material_data()

    def load_material_data(self):
        # 连接到SQLite数据库并查询材料表
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        cursor.execute('SELECT code, name, packaging_price, expiration_date FROM materials')
        materials = cursor.fetchall()

        # 清空表格内容
        self.material_table.setRowCount(0)

        # 填充表格
        for material in materials:
            row_position = self.material_table.rowCount()
            self.material_table.insertRow(row_position)
            for column, data in enumerate(material):
                self.material_table.setItem(row_position, column, QTableWidgetItem(str(data)))

        conn.close()

    def add_material(self):
        dialog = MaterialDialog(self, mode="add")
        dialog.exec_()
        self.load_material_data()  # 重新加载数据

    def edit_material(self):
        selected_row = self.material_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "警告", "请先选择一个材料！")
            return

        # 获取材料的编码，编码在第0列
        material_code = self.material_table.item(selected_row, 0).text()

        # 打开修改材料的对话框
        dialog = MaterialDialog(self, mode="edit", material_code=material_code)
        dialog.exec_()
        self.load_material_data()  # 重新加载数据

    def delete_material(self):
        selected_row = self.material_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "警告", "请先选择一个材料！")
            return

        # 获取材料的编码，编码在第0列
        material_code = self.material_table.item(selected_row, 0).text()

        # 删除材料的确认提示
        confirm = QMessageBox.question(self, "确认删除", f"确定要删除材料 编码为 {material_code} 吗？", 
                                       QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect('material.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM materials WHERE code = ?', (material_code,))
            conn.commit()
            conn.close()

            self.load_material_data()  # 重新加载数据


class MaterialDialog(QDialog):
    def __init__(self, parent=None, mode="add", material_code=None):
        super().__init__(parent)
        self.mode = mode
        self.material_code = material_code
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料" + ("增加" if self.mode == "add" else "修改"))
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout(self)
        form_layout = QGridLayout()

        # 编码
        self.code_label = QLabel("编码:")
        self.code_edit = QLineEdit()
        form_layout.addWidget(self.code_label, 0, 0)
        form_layout.addWidget(self.code_edit, 0, 1)

        # 名称
        self.name_label = QLabel("名称:")
        self.name_edit = QLineEdit()
        form_layout.addWidget(self.name_label, 1, 0)
        form_layout.addWidget(self.name_edit, 1, 1)

        # 包装价格
        self.price_label = QLabel("包装价格:")
        self.price_edit = QLineEdit()
        form_layout.addWidget(self.price_label, 2, 0)
        form_layout.addWidget(self.price_edit, 2, 1)

        # 失效日期
        self.expiration_label = QLabel("失效日期:")
        self.expiration_edit = QDateEdit()
        self.expiration_edit.setCalendarPopup(True)
        self.expiration_edit.setDate(QDate.currentDate())
        form_layout.addWidget(self.expiration_label, 3, 0)
        form_layout.addWidget(self.expiration_edit, 3, 1)

        # 确定和关闭按钮
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("确定")
        self.confirm_button.clicked.connect(self.save_material)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("关闭")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        if self.mode == "edit":
            self.load_material_data()

    def load_material_data(self):
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM materials WHERE code = ?', (self.material_code,))
        material = cursor.fetchone()
        conn.close()

        if material:
            self.code_edit.setText(material[1])  # 编码
            self.name_edit.setText(material[2])  # 名称
            self.price_edit.setText(str(material[3]))  # 包装价格
            self.expiration_edit.setDate(QDate.fromString(material[4], 'yyyy-MM-dd'))  # 失效日期

    def save_material(self):
        code = self.code_edit.text()
        name = self.name_edit.text()
        price = self.price_edit.text()
        expiration_date = self.expiration_edit.date().toString('yyyy-MM-dd')

        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        if self.mode == "add":
            cursor.execute('''
                INSERT INTO materials (code, name, packaging_price, expiration_date)
                VALUES (?, ?, ?, ?)
            ''', (code, name, price, expiration_date))
        elif self.mode == "edit":
            cursor.execute('''
                UPDATE materials 
                SET name = ?, packaging_price = ?, expiration_date = ?
                WHERE code = ?
            ''', (name, price, expiration_date, code))

        conn.commit()
        conn.close()

        self.close()
