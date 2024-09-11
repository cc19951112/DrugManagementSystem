import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, 
    QPushButton, QHBoxLayout, QDateEdit, QMessageBox, QCompleter
)
from PyQt5.QtCore import QDate, Qt


class MaterialOutboundDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料出库")
        self.setGeometry(300, 300, 500, 500)

        layout = QVBoxLayout(self)

        # 出库单号（自动生成，不可编辑）
        self.outbound_number_label = QLabel("出库单号:")
        self.outbound_number_edit = QLineEdit()
        self.outbound_number_edit.setReadOnly(True)  # 禁止手动修改出库单号
        layout.addWidget(self.outbound_number_label)
        layout.addWidget(self.outbound_number_edit)

        # 出库时间
        self.outbound_date_label = QLabel("出库时间:")
        self.outbound_date_edit = QDateEdit()
        self.outbound_date_edit.setCalendarPopup(True)
        self.outbound_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.outbound_date_label)
        layout.addWidget(self.outbound_date_edit)

        # 经办人
        self.handler_label = QLabel("经办人:")
        self.handler_edit = QLineEdit()
        layout.addWidget(self.handler_label)
        layout.addWidget(self.handler_edit)

        # 调拨科室（下拉选择）
        self.department_label = QLabel("调拨科室:")
        self.department_combo = QComboBox()
        self.department_combo.addItems(["妇科", "抽血", "B超", "心电图", "肺功能", 
                                        "放射科", "检验科", "内外科", "C14", "电测听"])
        layout.addWidget(self.department_label)
        layout.addWidget(self.department_combo)

        # 材料名称（关键词搜索）
        self.material_name_label = QLabel("材料名称:")
        self.material_name_edit = QLineEdit()
        layout.addWidget(self.material_name_label)
        layout.addWidget(self.material_name_edit)

        # 加载并设置自动完成器
        self.load_material_names()

        # 批号（只读）
        self.batch_number_label = QLabel("批号:")
        self.batch_number_edit = QLineEdit()
        self.batch_number_edit.setReadOnly(True)
        layout.addWidget(self.batch_number_label)
        layout.addWidget(self.batch_number_edit)

        # 失效日期（只读）
        self.expiration_date_label = QLabel("失效日期:")
        self.expiration_date_edit = QDateEdit()
        self.expiration_date_edit.setCalendarPopup(True)
        self.expiration_date_edit.setReadOnly(True)
        layout.addWidget(self.expiration_date_label)
        layout.addWidget(self.expiration_date_edit)

        # 售价（只读）
        self.selling_price_label = QLabel("售价:")
        self.selling_price_edit = QLineEdit()
        self.selling_price_edit.setReadOnly(True)
        layout.addWidget(self.selling_price_label)
        layout.addWidget(self.selling_price_edit)

        # 数量
        self.quantity_label = QLabel("数量:")
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 10000)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_spin)

        # 添加“保存”和“取消”按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # 连接按钮的信号与槽
        save_button.clicked.connect(self.save_outbound_record)
        cancel_button.clicked.connect(self.close)

        # 初始化时自动生成出库单号
        self.generate_outbound_number()

        # 绑定材料选择事件
        self.material_name_edit.textChanged.connect(self.load_material_details)

    def generate_outbound_number(self):
        """自动生成出库单号，格式为 YYYYMMDD + 三位流水号"""
        current_date = QDate.currentDate().toString('yyyyMMdd')  # 获取当前日期
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        # 查询当天已存在的最大单号编号
        cursor.execute('''
            SELECT MAX(CAST(SUBSTR(outbound_number, 9) AS INTEGER))
            FROM material_outbound
            WHERE SUBSTR(outbound_number, 1, 8) = ?
        ''', (current_date,))
        result = cursor.fetchone()

        if result[0] is not None:
            new_outbound_suffix = int(result[0]) + 1  # 自增1
        else:
            new_outbound_suffix = 1  # 当天第一个出库单号

        # 格式化为三位数字，生成新的出库单号
        new_outbound_number = f"{current_date}{new_outbound_suffix:03d}"
        self.outbound_number_edit.setText(new_outbound_number)

        conn.close()

    def load_material_names(self):
        """加载材料名称并设置自动完成器"""
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM materials')
        materials = [row[0] for row in cursor.fetchall()]
        conn.close()

        # 设置 QCompleter 实现关键词搜索功能
        completer = QCompleter(materials, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)  # 不区分大小写
        completer.setFilterMode(Qt.MatchContains)  # 模糊匹配
        self.material_name_edit.setCompleter(completer)

    def load_material_details(self):
        """从数据库加载选中材料的批号、失效日期和售价"""
        material_name = self.material_name_edit.text()

        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT batch_number, expiration_date, selling_price 
            FROM material_storage 
            WHERE material_name = ?
            ORDER BY storage_date DESC LIMIT 1
        ''', (material_name,))
        material_details = cursor.fetchone()
        conn.close()

        if material_details:
            self.batch_number_edit.setText(material_details[0])
            self.expiration_date_edit.setDate(QDate.fromString(material_details[1], 'yyyy-MM-dd'))
            self.selling_price_edit.setText(str(material_details[2]))

    def save_outbound_record(self):
        # 获取用户输入的数据
        outbound_number = self.outbound_number_edit.text()
        outbound_date = self.outbound_date_edit.date().toString('yyyy-MM-dd')
        handler = self.handler_edit.text()
        department = self.department_combo.currentText()  # 改为从下拉选择获取科室
        material_name = self.material_name_edit.text()
        batch_number = self.batch_number_edit.text()
        expiration_date = self.expiration_date_edit.date().toString('yyyy-MM-dd')
        selling_price = self.selling_price_edit.text()
        quantity = self.quantity_spin.value()

        # 连接到SQLite数据库
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        try:
            # 查询材料的库存
            cursor.execute('SELECT inventory_count FROM materials WHERE name = ?', (material_name,))
            material = cursor.fetchone()

            if material is None:
                print(f"材料 {material_name} 未找到，无法进行出库。")
                QMessageBox.warning(self, "错误", f"材料 {material_name} 未找到，无法进行出库。")
                return

            current_inventory = material[0]

            if current_inventory < quantity:
                # 如果库存不足，给出提示
                QMessageBox.warning(self, "错误", f"库存不足，当前库存为 {current_inventory}。")
                return

            # 插入出库记录到 material_outbound 表
            cursor.execute('''
                INSERT INTO material_outbound (outbound_number, outbound_date, handler, material_name, quantity, department, batch_number, expiration_date, selling_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (outbound_number, outbound_date, handler, material_name, quantity, department, batch_number, expiration_date, selling_price))

            # 更新 materials 表中的库存数量
            cursor.execute('''
                UPDATE materials 
                SET inventory_count = inventory_count - ?
                WHERE name = ?
            ''', (quantity, material_name))

            # 提交事务
            conn.commit()

            # 显示保存成功的提示
            QMessageBox.information(self, "成功", "材料出库记录已保存并更新库存！")

        except Exception as e:
            # 如果出现错误，则回滚事务
            conn.rollback()
            QMessageBox.warning(self, "错误", f"保存出库记录时出现错误: {str(e)}")

        finally:
            # 关闭数据库连接
            conn.close()

        # 关闭对话框
        self.close()
