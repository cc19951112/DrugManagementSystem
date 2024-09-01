import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QTabWidget
)
from PyQt5.QtCore import Qt, QDate

class DrugStorageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("药品入库 - 新开单据")
        self.setGeometry(200, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tab_document_info = QWidget()
        self.tab_detail_info = QWidget()

        self.tabs.addTab(self.tab_document_info, "单据信息")
        self.tabs.addTab(self.tab_detail_info, "明细信息")

        self.init_document_info_ui()
        self.init_detail_info_ui()

        layout.addWidget(self.tabs)

        # Buttons for save, print, and exit
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        print_button = QPushButton("打印")
        exit_button = QPushButton("退出")

        save_button.clicked.connect(self.save_document)
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(save_button)
        button_layout.addWidget(print_button)
        button_layout.addWidget(exit_button)
        layout.addLayout(button_layout)

    def init_document_info_ui(self):
        layout = QFormLayout(self.tab_document_info)

        # Input fields for document information
        self.document_number_edit = QLineEdit("RK20240830001")
        self.supplier_edit = QLineEdit()
        self.storage_method_combo = QComboBox()
        self.storage_method_combo.addItems(["普通入库", "急速入库"])
        self.storage_date_edit = QDateEdit(calendarPopup=True)
        self.storage_date_edit.setDate(QDate.currentDate())
        self.operator_edit = QLineEdit()
        self.responsible_edit = QLineEdit()
        self.opposite_responsible_edit = QLineEdit()
        self.remark_edit = QLineEdit()

        layout.addRow("入库单号:", self.document_number_edit)
        layout.addRow("供应商:", self.supplier_edit)
        layout.addRow("入库方式:", self.storage_method_combo)
        layout.addRow("入库时间:", self.storage_date_edit)
        layout.addRow("经手人:", self.operator_edit)
        layout.addRow("负责人:", self.responsible_edit)
        layout.addRow("对方负责人:", self.opposite_responsible_edit)
        layout.addRow("备注:", self.remark_edit)

    def init_detail_info_ui(self):
        layout = QVBoxLayout(self.tab_detail_info)

        # Table for detail information
        self.detail_table = QTableWidget(0, 18)  # Adjusted columns to match inventory structure
        self.detail_table.setHorizontalHeaderLabels([
            "序号", "名称", "规格", "产地", "批号",
            "失效日期", "生产日期","单位", "数量"
        ])
        self.detail_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.detail_table)

        # Detail input fields and add button
        detail_input_layout = QFormLayout()

        self.detail_drug_code_edit = QLineEdit()
        self.detail_name_edit = QLineEdit()
        self.detail_specification_edit = QLineEdit()
        self.detail_batch_edit = QLineEdit()
        self.detail_expiry_date_edit = QDateEdit(calendarPopup=True)
        self.detail_expiry_date_edit.setDate(QDate.currentDate())
        self.detail_production_date_edit = QDateEdit(calendarPopup=True)
        self.detail_production_date_edit.setDate(QDate.currentDate())
        self.detail_unit_edit = QLineEdit()
        self.detail_quantity_edit = QLineEdit()

        add_button = QPushButton("增加")
        add_button.clicked.connect(self.add_detail)

        detail_input_layout.addRow("药品编码:", self.detail_drug_code_edit)
        detail_input_layout.addRow("药品名称:", self.detail_name_edit)
        detail_input_layout.addRow("规格:", self.detail_specification_edit)
        detail_input_layout.addRow("批号:", self.detail_batch_edit)
        detail_input_layout.addRow("失效日期:", self.detail_expiry_date_edit)
        detail_input_layout.addRow("生产日期:", self.detail_production_date_edit)
        detail_input_layout.addRow("单位:", self.detail_unit_edit)
        detail_input_layout.addRow("数量:", self.detail_quantity_edit)

        detail_button_layout = QHBoxLayout()
        detail_button_layout.addStretch()
        detail_button_layout.addWidget(add_button)

        layout.addLayout(detail_input_layout)
        layout.addLayout(detail_button_layout)

    def add_detail(self):
        # Add the detail information to the table
        row_position = self.detail_table.rowCount()
        self.detail_table.insertRow(row_position)

        self.detail_table.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
        self.detail_table.setItem(row_position, 1, QTableWidgetItem(self.detail_drug_code_edit.text()))
        self.detail_table.setItem(row_position, 2, QTableWidgetItem(self.detail_name_edit.text()))
        self.detail_table.setItem(row_position, 3, QTableWidgetItem(self.detail_specification_edit.text()))
        self.detail_table.setItem(row_position, 4, QTableWidgetItem(self.detail_batch_edit.text()))
        self.detail_table.setItem(row_position, 5, QTableWidgetItem(self.detail_expiry_date_edit.text()))
        self.detail_table.setItem(row_position, 6, QTableWidgetItem(self.detail_production_date_edit.text()))
        self.detail_table.setItem(row_position, 7, QTableWidgetItem(self.detail_unit_edit.text()))
        self.detail_table.setItem(row_position, 8, QTableWidgetItem(self.detail_quantity_edit.text()))

    def save_document(self):
        # Save the document information to the database
        drug_code = self.document_number_edit.text()
        supplier = self.supplier_edit.text()
        storage_method = self.storage_method_combo.currentText()
        storage_date = self.storage_date_edit.date().toString(Qt.ISODate)
        operator = self.operator_edit.text()
        responsible = self.responsible_edit.text()
        opposite_responsible = self.opposite_responsible_edit.text()
        remark = self.remark_edit.text()

        conn = sqlite3.connect('drug_storage.db')
        cursor = conn.cursor()

        # Save the document info
        cursor.execute('''
            INSERT INTO documents (drug_code, supplier, storage_method, storage_date, 
                                   operator, responsible, opposite_responsible, remark)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (drug_code, supplier, storage_method, storage_date, operator, responsible, opposite_responsible, remark))

        # Save the details
        document_id = cursor.lastrowid  # Get the ID of the saved document
        for row in range(self.detail_table.rowCount()):
            drug_code = self.detail_table.item(row, 1).text()
            drug_name = self.detail_table.item(row, 2).text()
            specification = self.detail_table.item(row, 3).text()
            batch_number = self.detail_table.item(row, 4).text()
            expiration_date = self.detail_table.item(row, 5).text()
            production_date = self.detail_table.item(row, 6).text()
            unit = self.detail_table.item(row, 7).text()
            quantity = self.detail_table.item(row, 8).text()

            cursor.execute('''
                INSERT INTO inventory (drug_code, drug_name, specification, origin, batch_number, production_batch, 
                                       unit, stock, drug_sale_price, sale_amount, drug_purchase_price, purchase_amount, 
                                       gross_profit, gross_profit_rate, expiration_date, usage_period, insurance_code, 
                                       insurance_name, supplier)
                VALUES (?, ?, ?, '', ?, ?, ?, ?, 0, 0, 0, 0, 0, 0, ?, '', '', '', ?)
            ''', (drug_code, drug_name, specification, batch_number, production_date, unit, quantity, expiration_date, supplier))

        conn.commit()
        conn.close()

        self.accept()

def open_drug_storage_action(self):
    dialog = DrugStorageDialog(self)
    dialog.exec_()
