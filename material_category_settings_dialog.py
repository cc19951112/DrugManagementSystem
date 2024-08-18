import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, 
    QLabel, QLineEdit, QPushButton, QWidget, QSplitter, QGridLayout, QFrame
)

class MaterialCategorySettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("材料分类设置")
        self.setGeometry(200, 200, 600, 400)  # 修改窗口大小
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建上部的主分割器
        splitter = QSplitter(self)

        # 左侧材料分类树结构
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabels(["序号", "材料分类"])
        self.populate_category_tree()
        splitter.addWidget(self.category_tree)

        # 右侧材料分类详细信息布局
        details_widget = QWidget()
        details_layout = QGridLayout(details_widget)
        splitter.addWidget(details_widget)

        # 在右侧布局方式排列控件
        self.name_label = QLabel("名称:")
        self.name_edit = QLineEdit()
        details_layout.addWidget(self.name_label, 0, 0)
        details_layout.addWidget(self.name_edit, 0, 1, 1, 3)

        # 将分割器加入主布局
        main_layout.addWidget(splitter)

        # 设置底部按钮布局
        button_layout = QHBoxLayout()
        add_button = QPushButton("增加")
        edit_button = QPushButton("修改")
        delete_button = QPushButton("删除")
        confirm_button = QPushButton("确定")
        exit_button = QPushButton("退出")

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(exit_button)

        main_layout.addLayout(button_layout)

        # 绑定按钮到相应的操作函数
        add_button.clicked.connect(self.add_category)
        edit_button.clicked.connect(self.update_category)
        delete_button.clicked.connect(self.delete_category)
        confirm_button.clicked.connect(self.confirm_selection)
        exit_button.clicked.connect(self.close)
        
        # 绑定树形控件的item点击事件
        self.category_tree.itemClicked.connect(self.display_category_name)

    def populate_category_tree(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        # 清空树形控件
        self.category_tree.clear()

        # 查询材料分类
        cursor.execute("SELECT id, name FROM material_categories WHERE parent_id IS NULL")
        root_categories = cursor.fetchall()

        for index, (root_id, root_name) in enumerate(root_categories, start=1):
            root_item = QTreeWidgetItem(self.category_tree, [str(index), root_name])
            self.add_child_items(cursor, root_item, root_id, prefix=f"{index}.")

        # 展开所有节点
        self.category_tree.expandAll()

        # 关闭数据库连接
        conn.close()

    def add_child_items(self, cursor, parent_item, parent_id, prefix):
        # 查询子分类（parent_id 为父级分类的 id）
        cursor.execute("SELECT id, name FROM material_categories WHERE parent_id=?", (parent_id,))
        child_categories = cursor.fetchall()

        for index, (child_id, child_name) in enumerate(child_categories, start=1):
            child_item = QTreeWidgetItem(parent_item, [f"{prefix}{index}", child_name])
            # 递归添加子项
            self.add_child_items(cursor, child_item, child_id, prefix=f"{prefix}{index}.")

    def generate_unique_name(self, base_name):
        # 连接到SQLite数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        # 查询数据库中是否已经存在相同的名称
        cursor.execute("SELECT name FROM material_categories WHERE name LIKE ?", (base_name + '%',))
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

    def add_category(self):
        # 添加新分类
        name = self.name_edit.text()
        unique_name = self.generate_unique_name(name)

        # 插入到数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO material_categories (name, parent_id)
        VALUES (?, NULL)''', (unique_name,))

        conn.commit()
        conn.close()

        # 更新UI
        self.populate_category_tree()

    def update_category(self):
        # 修改分类
        selected_item = self.category_tree.currentItem()
        if selected_item:
            new_name = self.name_edit.text()
            unique_name = self.generate_unique_name(new_name)
            old_name = selected_item.text(1)

            conn = sqlite3.connect('materials.db')
            cursor = conn.cursor()

            cursor.execute('''
            UPDATE material_categories 
            SET name=? 
            WHERE name=?''', (unique_name, old_name))

            conn.commit()
            conn.close()

            # 更新UI
            self.populate_category_tree()

    def delete_category(self):
        # 删除分类
        selected_item = self.category_tree.currentItem()
        if selected_item:
            name = selected_item.text(1)

            conn = sqlite3.connect('materials.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM material_categories WHERE name=?', (name,))

            conn.commit()
            conn.close()

            # 更新UI
            self.populate_category_tree()

    def confirm_selection(self):
        # 确定选择的分类
        # todo: 逻辑实现
        pass

    def display_category_name(self, item):
        # 显示当前选中的分类名称
        self.name_edit.setText(item.text(1))  # 更新为第二列的内容
