import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, 
    QPushButton, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate

class MaterialStorageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("材料入库")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout(self)

        # 入库单号
        self.storage_number_label = QLabel("入库单号:")
        self.storage_number_edit = QLineEdit()
        layout.addWidget(self.storage_number_label)
        layout.addWidget(self.storage_number_edit)

        # 入库时间
        self.storage_date_label = QLabel("入库时间:")
        self.storage_date_edit = QDateEdit()
        self.storage_date_edit.setCalendarPopup(True)
        self.storage_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.storage_date_label)
        layout.addWidget(self.storage_date_edit)

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

        # 供应商
        self.supplier_label = QLabel("供应商:")
        self.supplier_edit = QLineEdit()
        layout.addWidget(self.supplier_label)
        layout.addWidget(self.supplier_edit)

        # 数量
        self.quantity_label = QLabel("数量:")
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 10000)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_spin)

        # 材料进价
        self.purchase_price_label = QLabel("材料进价:")
        self.purchase_price_edit = QLineEdit()
        layout.addWidget(self.purchase_price_label)
        layout.addWidget(self.purchase_price_edit)

        # 添加“保存”和“取消”按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # 连接按钮的信号与槽
        save_button.clicked.connect(self.save_storage_record)
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

    def save_storage_record(self):
        # 获取用户输入的数据
        storage_number = self.storage_number_edit.text()
        storage_date = self.storage_date_edit.date().toString('yyyy-MM-dd')
        handler = self.handler_edit.text()
        material_name = self.material_name_combo.currentText()
        supplier = self.supplier_edit.text()
        quantity = self.quantity_spin.value()
        purchase_price = self.purchase_price_edit.text()

        # 连接到SQLite数据库
        conn = sqlite3.connect('material.db')
        cursor = conn.cursor()

        try:
            # 插入入库记录到 material_storage 表
            cursor.execute('''
                INSERT INTO material_storage (storage_number, storage_date, handler, material_name, supplier, quantity, purchase_price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (storage_number, storage_date, handler, material_name, supplier, quantity, purchase_price))

            # 查询材料名称是否存在
            cursor.execute('SELECT * FROM materials WHERE name = ?', (material_name,))
            material = cursor.fetchone()
            if material is None:
                print(f"材料 {material_name} 未找到，库存无法更新。")
            else:
                print(f"材料 {material_name} 找到，开始更新库存。")

                # 更新 materials 表中的库存数量
                cursor.execute('''
                    UPDATE materials 
                    SET inventory_count = inventory_count + ?
                    WHERE name = ?
                ''', (quantity, material_name))

                # 提交事务
                conn.commit()
                print("Transaction committed successfully.")

                # 显示保存成功的提示
                QMessageBox.information(self, "成功", "材料入库记录已保存并更新库存！")

        except Exception as e:
            # 如果出现错误，则回滚事务
            conn.rollback()
            QMessageBox.warning(self, "错误", f"保存入库记录时出现错误: {str(e)}")

        finally:
            # 关闭数据库连接
            conn.close()


        # 关闭对话框
        self.close()
