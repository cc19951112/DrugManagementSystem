import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLabel, QLineEdit, QPushButton, QGridLayout
)

class MaterialAttributesSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("材料属性设置")
        self.setGeometry(200, 200, 800, 600)  # 修改窗口大小
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建材料属性表格
        self.attributes_table = QTableWidget(0, 2)
        self.attributes_table.setHorizontalHeaderLabels(["编码", "名称"])
        self.populate_attributes_table()
        main_layout.addWidget(self.attributes_table)

        # 创建名称和编码输入框
        form_layout = QGridLayout()
        self.code_label = QLabel("编码")
        self.code_edit = QLineEdit()
        self.name_label = QLabel("名称")
        self.name_edit = QLineEdit()

        form_layout.addWidget(self.code_label, 0, 0)
        form_layout.addWidget(self.code_edit, 0, 1)
        form_layout.addWidget(self.name_label, 1, 0)
        form_layout.addWidget(self.name_edit, 1, 1)

        main_layout.addLayout(form_layout)

        # 创建底部按钮布局
        button_layout = QHBoxLayout()
        add_button = QPushButton("增加")
        edit_button = QPushButton("修改")
        delete_button = QPushButton("删除")
        confirm_button = QPushButton("确定")
        print_button = QPushButton("打印")
        export_button = QPushButton("转Excel")
        help_button = QPushButton("帮助")
        exit_button = QPushButton("退出")

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(print_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(help_button)
        button_layout.addWidget(exit_button)

        main_layout.addLayout(button_layout)

        # 绑定按钮到相应的操作函数
        add_button.clicked.connect(self.add_attribute)
        edit_button.clicked.connect(self.update_attribute)
        delete_button.clicked.connect(self.delete_attribute)
        confirm_button.clicked.connect(self.confirm_selection)
        exit_button.clicked.connect(self.close)

        # 将主布局设置为对话框的布局
        self.setLayout(main_layout)

        # 绑定表格点击事件，点击时在编辑框中显示选中的编码和名称
        self.attributes_table.cellClicked.connect(self.display_attribute_details)

    def populate_attributes_table(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        # 查询材料属性
        cursor.execute("SELECT code, name FROM material_attributes")
        attributes = cursor.fetchall()

        self.attributes_table.setRowCount(0)  # 清空表格

        for attribute in attributes:
            row_position = self.attributes_table.rowCount()
            self.attributes_table.insertRow(row_position)
            self.attributes_table.setItem(row_position, 0, QTableWidgetItem(attribute[0]))
            self.attributes_table.setItem(row_position, 1, QTableWidgetItem(attribute[1]))

        # 关闭数据库连接
        conn.close()

    def generate_unique_code(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        # 查询数据库中所有的编码并将其转为整数列表
        cursor.execute("SELECT code FROM material_attributes")
        existing_codes = cursor.fetchall()

        conn.close()

        # 提取最大值的编码并生成新的编码
        existing_codes = [int(code[0]) for code in existing_codes if code[0].isdigit()]
        max_code = max(existing_codes) if existing_codes else 0
        new_code = str(max_code + 1)

        return new_code

    def generate_unique_name(self, base_name):
        # 连接到SQLite数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        # 查询数据库中是否已经存在相同的名称
        cursor.execute("SELECT name FROM material_attributes WHERE name LIKE ?", (base_name + '%',))
        existing_names = cursor.fetchall()

        conn.close()

        if not existing_names:
            return base_name

        # 提取已有名称的后缀编号，生成新的编号
        max_suffix = 1
        for name in existing_names:
            if name[0] == base_name:
                continue
            suffix = name[0].replace(base_name + '_', '')
            if suffix.isdigit():
                max_suffix = max(max_suffix, int(suffix) + 1)

        return f"{base_name}_{max_suffix}"

    def add_attribute(self):
        # 添加新材料属性
        base_code = self.code_edit.text()
        base_name = self.name_edit.text()

        # 生成唯一编码和名称
        unique_code = base_code if base_code and not self.check_code_exists(base_code) else self.generate_unique_code()
        unique_name = self.generate_unique_name(base_name)

        # 插入到数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO material_attributes (code, name)
        VALUES (?, ?)''', (unique_code, unique_name))

        conn.commit()
        conn.close()

        # 更新UI
        self.populate_attributes_table()

    def update_attribute(self):
        # 修改材料属性
        selected_row = self.attributes_table.currentRow()
        if selected_row != -1:
            old_code = self.attributes_table.item(selected_row, 0).text()

            base_code = self.code_edit.text()
            base_name = self.name_edit.text()

            # 生成唯一编码和名称
            unique_code = base_code if base_code and not (base_code != old_code and self.check_code_exists(base_code)) else self.generate_unique_code()
            unique_name = self.generate_unique_name(base_name)

            conn = sqlite3.connect('materials.db')
            cursor = conn.cursor()

            cursor.execute('''
            UPDATE material_attributes 
            SET code=?, name=? 
            WHERE code=?''', (unique_code, unique_name, old_code))

            conn.commit()
            conn.close()

            # 更新UI
            self.populate_attributes_table()

    def check_code_exists(self, code):
        # 检查编码是否已经存在
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM material_attributes WHERE code=?", (code,))
        exists = cursor.fetchone()[0] > 0

        conn.close()
        return exists

    def delete_attribute(self):
        # 删除材料属性
        selected_row = self.attributes_table.currentRow()
        if selected_row != -1:
            code = self.attributes_table.item(selected_row, 0).text()

            conn = sqlite3.connect('materials.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM material_attributes WHERE code=?', (code,))

            conn.commit()
            conn.close()

            # 更新UI
            self.populate_attributes_table()

    def confirm_selection(self):
        # 确定选择的属性
        # todo: 实现逻辑
        pass

    def display_attribute_details(self, row, column):
        # 在点击表格中的条目时，显示相应的编码和名称在编辑框中
        code = self.attributes_table.item(row, 0).text()
        name = self.attributes_table.item(row, 1).text()
        self.code_edit.setText(code)
        self.name_edit.setText(name)
