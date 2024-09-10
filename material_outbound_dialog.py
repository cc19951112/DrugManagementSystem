import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, 
    QPushButton, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate


class MaterialOutboundDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料出库")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout(self)

        # 出库单号
        self.outbound_number_label = QLabel("出库单号:")
        self.outbound_number_edit = QLineEdit()
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

        # 材料名称（从材料表中提取数据）
        self.material_name_label = QLabel("材料名称:")
        self.material_name_combo = QComboBox()
        self.load_material_names()
        layout.addWidget(self.material_name_label)
        layout.addWidget(self.material_name_combo)

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

    def load_material_names(self):
        """从数据库加载所有材料名称到下拉框"""
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM materials')
        materials = cursor.fetchall()
        conn.close()

        for material in materials:
            self.material_name_combo.addItem(material[0])

    def save_outbound_record(self):
        # 获取用户输入的数据
        outbound_number = self.outbound_number_edit.text()
        outbound_date = self.outbound_date_edit.date().toString('yyyy-MM-dd')
        handler = self.handler_edit.text()
        material_name = self.material_name_combo.currentText()
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
                INSERT INTO material_outbound (outbound_number, outbound_date, handler, material_name, quantity)
                VALUES (?, ?, ?, ?, ?)
            ''', (outbound_number, outbound_date, handler, material_name, quantity))

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
