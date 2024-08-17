from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, 
    QLabel, QLineEdit, QPushButton, QWidget, QSplitter, QGridLayout, QFrame, QCompleter
)
import sqlite3

class SupplierSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("供应商设置")
        self.setGeometry(200, 200, 800, 600)  # 修改窗口大小
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建搜索框和QCompleter
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入供应商名称搜索...")

        # 初始化 QCompleter
        self.completer = QCompleter(self)
        self.search_edit.setCompleter(self.completer)
        self.search_edit.textEdited.connect(self.update_completer)  # 当编辑时实时更新

        search_button = QPushButton("搜索")
        search_button.clicked.connect(self.search_supplier)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_button)

        # 将搜索布局添加到主布局
        main_layout.addLayout(search_layout)

        # 创建上部的主分割器
        splitter = QSplitter(self)

        # 左侧供应商树结构
        self.supplier_tree = QTreeWidget()
        self.supplier_tree.setHeaderLabel("供应商列表")
        self.populate_supplier_tree()
        splitter.addWidget(self.supplier_tree)

        # 右侧供应商详细信息布局
        details_widget = QWidget()
        details_layout = QGridLayout(details_widget)
        splitter.addWidget(details_widget)

        # 在右侧按图中的布局方式排列控件
        self.name_label = QLabel("名称:")
        self.name_edit = QLineEdit()
        self.wb_code_label = QLabel("五笔码:")
        self.wb_code_edit = QLineEdit()
        self.py_code_label = QLabel("拼音码:")
        self.py_code_edit = QLineEdit()
        self.address_label = QLabel("地址:")
        self.address_edit = QLineEdit()
        self.email_label = QLabel("邮箱:")
        self.email_edit = QLineEdit()
        self.fax_label = QLabel("传真:")
        self.fax_edit = QLineEdit()
        self.phone_label = QLabel("电话:")
        self.phone_edit = QLineEdit()
        self.contact_label = QLabel("联系人:")
        self.contact_edit = QLineEdit()
        self.bank_label = QLabel("开户行:")
        self.bank_edit = QLineEdit()
        self.account_label = QLabel("帐号:")
        self.account_edit = QLineEdit()
        self.tax_label = QLabel("税号:")
        self.tax_edit = QLineEdit()
        self.note_label = QLabel("备注:")
        self.note_edit = QLineEdit()

        # 按照图中的布局设置控件的位置
        details_layout.addWidget(self.name_label, 0, 0)
        details_layout.addWidget(self.name_edit, 0, 1, 1, 3)
        details_layout.addWidget(self.address_label, 0, 4)
        details_layout.addWidget(self.address_edit, 0, 5)

        details_layout.addWidget(self.wb_code_label, 1, 0)
        details_layout.addWidget(self.wb_code_edit, 1, 1, 1, 3)
        details_layout.addWidget(self.py_code_label, 1, 4)
        details_layout.addWidget(self.py_code_edit, 1, 5)

        details_layout.addWidget(self.email_label, 2, 0)
        details_layout.addWidget(self.email_edit, 2, 1, 1, 3)
        details_layout.addWidget(self.fax_label, 2, 4)
        details_layout.addWidget(self.fax_edit, 2, 5)

        details_layout.addWidget(self.phone_label, 3, 0)
        details_layout.addWidget(self.phone_edit, 3, 1, 1, 5)

        details_layout.addWidget(self.contact_label, 4, 0)
        details_layout.addWidget(self.contact_edit, 4, 1, 1, 5)

        details_layout.addWidget(self.bank_label, 5, 0)
        details_layout.addWidget(self.bank_edit, 5, 1, 1, 3)
        details_layout.addWidget(self.account_label, 5, 4)
        details_layout.addWidget(self.account_edit, 5, 5)

        details_layout.addWidget(self.tax_label, 6, 0)
        details_layout.addWidget(self.tax_edit, 6, 1, 1, 5)

        details_layout.addWidget(self.note_label, 7, 0)
        details_layout.addWidget(self.note_edit, 7, 1, 1, 5)

        # 加入分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        details_layout.addWidget(line, 8, 0, 1, 6)

        # 将分割器加入主布局
        main_layout.addWidget(splitter)

        # 设置底部按钮布局
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
        add_button.clicked.connect(self.add_supplier)
        edit_button.clicked.connect(self.update_supplier)
        delete_button.clicked.connect(self.delete_supplier)
        confirm_button.clicked.connect(self.update_supplier)  # 可与修改按钮绑定同一功能
        self.supplier_tree.itemClicked.connect(self.display_supplier_details)

    def populate_supplier_tree(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('suppliers.db')
        cursor = conn.cursor()

        # 清空树
        self.supplier_tree.clear()

        # 查询根供应商（parent_id 为 NULL）
        cursor.execute("SELECT id, name FROM suppliers WHERE parent_id IS NULL")
        root_suppliers = cursor.fetchall()

        for root_id, root_name in root_suppliers:
            root_item = QTreeWidgetItem(self.supplier_tree, [root_name])
            self.add_child_items(cursor, root_item, root_id)

        # 展开所有节点
        self.supplier_tree.expandAll()

        # 关闭数据库连接
        conn.close()

    def add_child_items(self, cursor, parent_item, parent_id):
        # 查询子供应商（parent_id 为父级供应商的 id）
        cursor.execute("SELECT id, name FROM suppliers WHERE parent_id=?", (parent_id,))
        child_suppliers = cursor.fetchall()

        for child_id, child_name in child_suppliers:
            child_item = QTreeWidgetItem(parent_item, [child_name])
            # 递归添加子项
            self.add_child_items(cursor, child_item, child_id)

    def add_supplier(self):
        name = self.name_edit.text()
        wb_code = self.wb_code_edit.text()
        py_code = self.py_code_edit.text()
        address = self.address_edit.text()
        email = self.email_edit.text()
        fax = self.fax_edit.text()
        phone = self.phone_edit.text()
        contact = self.contact_edit.text()
        bank = self.bank_edit.text()
        account = self.account_edit.text()
        tax = self.tax_edit.text()
        note = self.note_edit.text()

        conn = sqlite3.connect('suppliers.db')
        cursor = conn.cursor()

        # 检查是否存在同名供应商
        cursor.execute('SELECT COUNT(*) FROM suppliers WHERE name LIKE ?', (name + '%',))
        count = cursor.fetchone()[0]

        # 如果存在同名供应商，加上序号
        if count > 0:
            name = f"{name}_{count+1}"

        cursor.execute('''
            INSERT INTO suppliers (name, wb_code, py_code, address, email, fax, phone, contact, bank, account, tax, note, parent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)''', 
            (name, wb_code, py_code, address, email, fax, phone, contact, bank, account, tax, note))
        
        conn.commit()
        conn.close()

        # 更新UI
        self.populate_supplier_tree()

    def delete_supplier(self):
        selected_item = self.supplier_tree.currentItem()
        if selected_item:
            name = selected_item.text(0)
            
            conn = sqlite3.connect('suppliers.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM suppliers WHERE name=?', (name,))
            
            conn.commit()
            conn.close()

            # 更新UI
            self.populate_supplier_tree()

    def update_supplier(self):
        selected_item = self.supplier_tree.currentItem()
        if selected_item:
            name = selected_item.text(0)

            new_name = self.name_edit.text()
            wb_code = self.wb_code_edit.text()
            py_code = self.py_code_edit.text()
            address = self.address_edit.text()
            email = self.email_edit.text()
            fax = self.fax_edit.text()
            phone = self.phone_edit.text()
            contact = self.contact_edit.text()
            bank = self.bank_edit.text()
            account = self.account_edit.text()
            tax = self.tax_edit.text()
            note = self.note_edit.text()

            conn = sqlite3.connect('suppliers.db')
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE suppliers 
                SET name=?, wb_code=?, py_code=?, address=?, email=?, fax=?, phone=?, contact=?, bank=?, account=?, tax=?, note=? 
                WHERE name=?''',
                (new_name, wb_code, py_code, address, email, fax, phone, contact, bank, account, tax, note, name))

            conn.commit()
            conn.close()

            # 更新UI
            self.populate_supplier_tree()

    def display_supplier_details(self, item):
        name = item.text(0)

        conn = sqlite3.connect('suppliers.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM suppliers WHERE name=?', (name,))
        supplier = cursor.fetchone()

        conn.close()

        if supplier:
            # 将查询到的供应商详细信息填充到输入框
            self.name_edit.setText(supplier[1])
            self.wb_code_edit.setText(supplier[2])
            self.py_code_edit.setText(supplier[3])
            self.address_edit.setText(supplier[4])
            self.email_edit.setText(supplier[5])
            self.fax_edit.setText(supplier[6])
            self.phone_edit.setText(supplier[7])
            self.contact_edit.setText(supplier[8])
            self.bank_edit.setText(supplier[9])
            self.account_edit.setText(supplier[10])
            self.tax_edit.setText(supplier[11])
            self.note_edit.setText(supplier[12])

    def search_supplier(self):
        search_text = self.search_edit.text().strip()

        if not search_text:
            self.populate_supplier_tree()  # 如果搜索栏为空，则显示所有供应商
            return

        # 连接到SQLite数据库
        conn = sqlite3.connect('suppliers.db')
        cursor = conn.cursor()

        # 清空树
        self.supplier_tree.clear()

        # 查询匹配的供应商（名称中包含搜索文本）
        cursor.execute("SELECT id, name FROM suppliers WHERE name LIKE ?", ('%' + search_text + '%',))
        matching_suppliers = cursor.fetchall()

        for supplier_id, supplier_name in matching_suppliers:
            supplier_item = QTreeWidgetItem(self.supplier_tree, [supplier_name])
            self.add_child_items(cursor, supplier_item, supplier_id)

        # 展开所有节点
        self.supplier_tree.expandAll()

        # 关闭数据库连接
        conn.close()

    def update_completer(self, text):
        if not text:
            return

        # 连接到SQLite数据库
        conn = sqlite3.connect('suppliers.db')
        cursor = conn.cursor()

        # 查询匹配的供应商名称
        cursor.execute("SELECT name FROM suppliers WHERE name LIKE ?", ('%' + text + '%',))
        matching_names = [row[0] for row in cursor.fetchall()]

        # 更新 QCompleter 的模型
        self.completer.setModel(self.create_model(matching_names))

        conn.close()

    def create_model(self, names):
        from PyQt5.QtCore import QStringListModel
        model = QStringListModel()
        model.setStringList(names)
        return model
