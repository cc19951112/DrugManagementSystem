import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSplitter, QTreeWidget, QTreeWidgetItem, 
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout,
    QDialog, QLabel, QLineEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QFrame
)

class MaterialSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建主分割器，用于分隔左侧的树形控件和右侧的表格
        splitter = QSplitter(Qt.Horizontal)

        # 左侧材料分类树结构
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabel("材料分类")
        self.populate_category_tree()
        splitter.addWidget(self.category_tree)

        # 右侧材料详细信息表格
        self.material_table = QTableWidget(0, 18)  # 设置列数为18，以包含所有字段
        self.material_table.setHorizontalHeaderLabels([
            "序号", "分类", "编码", "名称", "规格", "产地", "属性", 
            "费用", "拼音码", "五笔码", "包装单位", "使用单位", 
            "包装换算", "包装批价", "使用批价", "包装售价", "使用售价", "生产厂家"
        ])
        self.material_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.material_table.setShowGrid(True)  # 显示网格线
        splitter.addWidget(self.material_table)

        # 设置左侧和右侧的比例，3:7
        splitter.setStretchFactor(0, 1) 
        splitter.setStretchFactor(1, 7)  

        # 将分割器加入主布局
        main_layout.addWidget(splitter)

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

        # 绑定树形控件的item点击事件
        self.category_tree.itemClicked.connect(self.filter_materials_by_category)

    def populate_category_tree(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        # 清空树形控件
        self.category_tree.clear()

        # 添加“全部分类”根节点
        all_categories_item = QTreeWidgetItem(self.category_tree, ["全部分类"])
        self.category_tree.addTopLevelItem(all_categories_item)

        # 查询材料分类
        cursor.execute("SELECT id, name FROM material_categories WHERE parent_id IS NULL")
        root_categories = cursor.fetchall()

        for root_id, root_name in root_categories:
            root_item = QTreeWidgetItem(self.category_tree, [root_name])
            self.add_child_items(cursor, root_item, root_id)

        # 展开所有节点
        self.category_tree.expandAll()

        # 关闭数据库连接
        conn.close()

    def add_child_items(self, cursor, parent_item, parent_id):
        # 查询子分类（parent_id 为父级分类的 id）
        cursor.execute("SELECT id, name FROM material_categories WHERE parent_id=?", (parent_id,))
        child_categories = cursor.fetchall()

        for child_id, child_name in child_categories:
            child_item = QTreeWidgetItem(parent_item, [child_name])
            # 递归添加子项
            self.add_child_items(cursor, child_item, child_id)

    def filter_materials_by_category(self, item):
        # 获取选中的分类名称
        category_name = item.text(0)

        # 连接到SQLite数据库并查询材料表
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        if category_name == "全部分类":
            cursor.execute('SELECT * FROM materials')
        else:
            cursor.execute('SELECT * FROM materials WHERE category = ?', (category_name,))

        materials = cursor.fetchall()

        # 清空表格内容（除表头外）
        self.material_table.setRowCount(0)

        # 检查是否有查询结果
        if materials:
            # 填充表格
            for material in materials:
                row_position = self.material_table.rowCount()
                self.material_table.insertRow(row_position)
                for column, data in enumerate(material):
                    self.material_table.setItem(row_position, column, QTableWidgetItem(str(data)))
        else:
            # 没有查询结果时，只保留表头
            self.material_table.clearContents()

        conn.close()

    def add_material(self):
        # 检查是否选择了某个分类
        selected_item = self.category_tree.currentItem()
        if not selected_item or selected_item.text(0) == "全部分类":
            QMessageBox.warning(self, "警告", "请先选择一个分类！")
            return

        # 打开增加材料的对话框
        dialog = MaterialDialog(self, mode="add", category=selected_item.text(0))
        dialog.exec_()
        self.filter_materials_by_category(selected_item)  # 刷新表格

    def edit_material(self):
        # 检查是否选择了某个材料
        selected_row = self.material_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "警告", "请先选择一个材料！")
            return

        # 获取当前材料的分类和编码
        category = self.material_table.item(selected_row, 1).text()
        code = self.material_table.item(selected_row, 2).text()

        # 打开修改材料的对话框
        dialog = MaterialDialog(self, mode="edit", category=category, code=code)
        dialog.exec_()
        self.filter_materials_by_category(self.category_tree.currentItem())  # 刷新表格

    def delete_material(self):
        # 检查是否选择了某个材料
        selected_row = self.material_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "警告", "请先选择一个材料！")
            return

        # 获取当前材料的编码
        code = self.material_table.item(selected_row, 2).text()

        # 删除材料
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM materials WHERE code = ?', (code,))
        conn.commit()
        conn.close()

        # 刷新表格
        self.filter_materials_by_category(self.category_tree.currentItem())

class MaterialDialog(QDialog):
    def __init__(self, parent=None, mode="add", category=None, code=None):
        super().__init__(parent)
        self.mode = mode
        self.category = category
        self.code = code
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料" + ("增加" if self.mode == "add" else "修改"))
        self.setGeometry(200, 200, 800, 600)

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
        form_layout.addWidget(self.name_label, 0, 2)
        form_layout.addWidget(self.name_edit, 0, 3)

        # 五笔码
        self.wbm_label = QLabel("五笔码:")
        self.wbm_edit = QLineEdit()
        form_layout.addWidget(self.wbm_label, 1, 0)
        form_layout.addWidget(self.wbm_edit, 1, 1)

        # 拼音码
        self.pym_label = QLabel("拼音码:")
        self.pym_edit = QLineEdit()
        form_layout.addWidget(self.pym_label, 1, 2)
        form_layout.addWidget(self.pym_edit, 1, 3)

        # 规格
        self.spec_label = QLabel("规格:")
        self.spec_edit = QLineEdit()
        form_layout.addWidget(self.spec_label, 2, 0)
        form_layout.addWidget(self.spec_edit, 2, 1)

        # 产地
        self.origin_label = QLabel("产地:")
        self.origin_edit = QLineEdit()
        form_layout.addWidget(self.origin_label, 2, 2)
        form_layout.addWidget(self.origin_edit, 2, 3)

        # 生产厂家
        self.manufacturer_label = QLabel("生产厂家:")
        self.manufacturer_edit = QLineEdit()
        form_layout.addWidget(self.manufacturer_label, 3, 0)
        form_layout.addWidget(self.manufacturer_edit, 3, 1, 1, 3)

        # 注册证号
        self.registration_label = QLabel("注册证号:")
        self.registration_edit = QLineEdit()
        form_layout.addWidget(self.registration_label, 4, 0)
        form_layout.addWidget(self.registration_edit, 4, 1)

        # 许可证号
        self.license_label = QLabel("许可证号:")
        self.license_edit = QLineEdit()
        form_layout.addWidget(self.license_label, 4, 2)
        form_layout.addWidget(self.license_edit, 4, 3)

        # 属性
        self.attribute_label = QLabel("属性:")
        self.attribute_combo = QComboBox()
        self.attribute_combo.addItems(["可重复使用器械类", "一次性器械类", "其它类"])  # 示例选项
        form_layout.addWidget(self.attribute_label, 5, 0)
        form_layout.addWidget(self.attribute_combo, 5, 1)

        # 剂型
        self.dosage_label = QLabel("剂型:")
        self.dosage_combo = QComboBox()
        self.dosage_combo.addItems(["无", "片剂", "注射剂"])  # 示例选项
        form_layout.addWidget(self.dosage_label, 5, 2)
        form_layout.addWidget(self.dosage_combo, 5, 3)

        # 费用类别
        self.cost_category_label = QLabel("费用类别:")
        self.cost_category_combo = QComboBox()
        self.cost_category_combo.addItems(["检查费", "治疗费"])  # 示例选项
        form_layout.addWidget(self.cost_category_label, 6, 0)
        form_layout.addWidget(self.cost_category_combo, 6, 1)

        # 包装单位
        self.packaging_unit_label = QLabel("包装单位:")
        self.packaging_unit_combo = QComboBox()
        self.packaging_unit_combo.addItems(["盒", "袋"])  # 示例选项
        form_layout.addWidget(self.packaging_unit_label, 7, 0)
        form_layout.addWidget(self.packaging_unit_combo, 7, 1)

        # 使用单位
        self.usage_unit_label = QLabel("使用单位:")
        self.usage_unit_combo = QComboBox()
        self.usage_unit_combo.addItems(["支", "片"])  # 示例选项
        form_layout.addWidget(self.usage_unit_label, 7, 2)
        form_layout.addWidget(self.usage_unit_combo, 7, 3)

        # 包装换算
        self.packaging_conversion_label = QLabel("包装换算:")
        self.packaging_conversion_edit = QLineEdit()
        form_layout.addWidget(self.packaging_conversion_label, 8, 0)
        form_layout.addWidget(self.packaging_conversion_edit, 8, 1)

        # 包装批价
        self.packaging_cost_label = QLabel("包装批价:")
        self.packaging_cost_edit = QLineEdit()
        form_layout.addWidget(self.packaging_cost_label, 8, 2)
        form_layout.addWidget(self.packaging_cost_edit, 8, 3)

        # 使用批价
        self.usage_cost_label = QLabel("使用批价:")
        self.usage_cost_edit = QLineEdit()
        form_layout.addWidget(self.usage_cost_label, 9, 0)
        form_layout.addWidget(self.usage_cost_edit, 9, 1)

        # 包装售价
        self.packaging_sale_label = QLabel("包装售价:")
        self.packaging_sale_edit = QLineEdit()
        form_layout.addWidget(self.packaging_sale_label, 9, 2)
        form_layout.addWidget(self.packaging_sale_edit, 9, 3)

        # 使用售价
        self.usage_sale_label = QLabel("使用售价:")
        self.usage_sale_edit = QLineEdit()
        form_layout.addWidget(self.usage_sale_label, 10, 0)
        form_layout.addWidget(self.usage_sale_edit, 10, 1)

        # 国家医保编码
        self.insurance_code_label = QLabel("国家医保编码:")
        self.insurance_code_edit = QLineEdit()
        form_layout.addWidget(self.insurance_code_label, 11, 0)
        form_layout.addWidget(self.insurance_code_edit, 11, 1)

        # 采购平台产品代码
        self.purchase_code_label = QLabel("采购平台产品代码:")
        self.purchase_code_edit = QLineEdit()
        form_layout.addWidget(self.purchase_code_label, 11, 2)
        form_layout.addWidget(self.purchase_code_edit, 11, 3)

        # 国家药品标准码
        self.drug_standard_label = QLabel("国家药品标准码:")
        self.drug_standard_edit = QLineEdit()
        form_layout.addWidget(self.drug_standard_label, 12, 0)
        form_layout.addWidget(self.drug_standard_edit, 12, 1)

        # 水平分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        form_layout.addWidget(line, 13, 0, 1, 4)

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

        # 如果是修改模式，填充原始数据
        if self.mode == "edit":
            self.load_material_data()

    def load_material_data(self):
        # 连接数据库并查询当前材料的信息
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM materials WHERE category = ? AND code = ?', (self.category, self.code))
        material = cursor.fetchone()
        conn.close()

        # 填充表单
        if material:
            self.code_edit.setText(material[2])
            self.name_edit.setText(material[3])
            self.wbm_edit.setText(material[4])
            self.pym_edit.setText(material[5])
            self.spec_edit.setText(material[6])
            self.origin_edit.setText(material[7])
            self.manufacturer_edit.setText(material[8])
            self.registration_edit.setText(material[9])
            self.license_edit.setText(material[10])
            self.attribute_combo.setCurrentText(material[11])
            self.dosage_combo.setCurrentText(material[12])
            self.cost_category_combo.setCurrentText(material[13])
            self.packaging_unit_combo.setCurrentText(material[14])
            self.usage_unit_combo.setCurrentText(material[15])
            self.packaging_conversion_edit.setText(material[16])
            self.packaging_cost_edit.setText(material[17])
            self.usage_cost_edit.setText(material[18])
            self.packaging_sale_edit.setText(material[19])
            self.usage_sale_edit.setText(material[20])
            self.insurance_code_edit.setText(material[21])
            self.purchase_code_edit.setText(material[22])
            self.drug_standard_edit.setText(material[23])

    def save_material(self):
        # 获取表单数据
        code = self.code_edit.text()
        name = self.name_edit.text()
        wbm = self.wbm_edit.text()
        pym = self.pym_edit.text()
        spec = self.spec_edit.text()
        origin = self.origin_edit.text()
        manufacturer = self.manufacturer_edit.text()
        registration = self.registration_edit.text()
        license = self.license_edit.text()
        attribute = self.attribute_combo.currentText()
        dosage = self.dosage_combo.currentText()
        cost_category = self.cost_category_combo.currentText()
        packaging_unit = self.packaging_unit_combo.currentText()
        usage_unit = self.usage_unit_combo.currentText()
        packaging_conversion = self.packaging_conversion_edit.text()
        packaging_cost = self.packaging_cost_edit.text()
        usage_cost = self.usage_cost_edit.text()
        packaging_sale = self.packaging_sale_edit.text()
        usage_sale = self.usage_sale_edit.text()
        insurance_code = self.insurance_code_edit.text()
        purchase_code = self.purchase_code_edit.text()
        drug_standard = self.drug_standard_edit.text()

        # 连接数据库并保存数据
        conn = sqlite3.connect('materials.db')
        cursor = conn.cursor()

        if self.mode == "add":
            cursor.execute('''
                INSERT INTO materials (
                    category, code, name, wb_code, pinyin, spec, origin, manufacturer, registration, license,
                    attribute, dosage, cost_category, package_unit, use_unit, packaging_conversion,
                    package_price, use_sale, packaging_sale, usage_sale, insurance_code, purchase_code, drug_standard
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (self.category, code, name, wbm, pym, spec, origin, manufacturer, registration, license,
                 attribute, dosage, cost_category, packaging_unit, usage_unit, packaging_conversion,
                 packaging_cost, usage_cost, packaging_sale, usage_sale, insurance_code, purchase_code, drug_standard))
        elif self.mode == "edit":
            cursor.execute('''
                UPDATE materials 
                SET name = ?, wb_code = ?, pinyin = ?, spec = ?, origin = ?, manufacturer = ?, registration = ?, license = ?, 
                    attribute = ?, dosage = ?, cost_category = ?, package_unit = ?, use_unit = ?, packaging_conversion = ?, 
                    package_price = ?, use_sale = ?, packaging_sale = ?, usage_sale = ?, insurance_code = ?, purchase_code = ?, drug_standard = ?
                WHERE category = ? AND code = ?''',
                (name, wbm, pym, spec, origin, manufacturer, registration, license, 
                 attribute, dosage, cost_category, packaging_unit, usage_unit, packaging_conversion, 
                 packaging_cost, usage_cost, packaging_sale, usage_sale, insurance_code, purchase_code, drug_standard, 
                 self.category, code))

        conn.commit()
        conn.close()

        self.close()