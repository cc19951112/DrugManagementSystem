# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStatusBar, QToolBar
# from supplier_settings_dialog import SupplierSettingsDialog  # 导入供应商设置对话框类
# from material_category_settings_dialog import MaterialCategorySettingsDialog  # 导入材料分类设置对话框类
# from material_attributes_settings_dialog import MaterialAttributesSettingsDialog
# from material_settings_dialog import MaterialSettingsDialog

# class DrugManagementSystem(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # 设置窗口标题和初始尺寸
#         self.setWindowTitle("药物管理系统")
#         self.setGeometry(100, 100, 1024, 768)

#         # 创建菜单栏
#         self.create_menus()

#         # 创建工具栏
#         self.create_toolbar()

#         # 创建状态栏
#         self.create_statusbar()

#         # 初始化UI
#         self.init_ui()

#     def create_menus(self):
#         # 创建菜单栏
#         menu_bar = self.menuBar()

#         # 系统管理菜单
#         system_management_menu = menu_bar.addMenu("系统管理(&S)")

#         # 基础信息设置菜单
#         basic_info_settings_menu = menu_bar.addMenu("基础信息设置(&B)")

#         # 业务信息设置菜单
#         business_info_settings_menu = menu_bar.addMenu("业务信息设置(&Y)")

#         # 门诊业务菜单
#         outpatient_business_menu = menu_bar.addMenu("门诊业务(&M)")

#         # 业务管理菜单
#         business_management_menu = menu_bar.addMenu("业务管理(&T)")

#         # 业务报表查询菜单
#         business_report_query_menu = menu_bar.addMenu("业务报表查询(&Q)")

#         # 库存报表查询菜单
#         inventory_report_query_menu = menu_bar.addMenu("库存报表查询(&R)")

#         # 门诊报表查询菜单
#         outpatient_report_query_menu = menu_bar.addMenu("门诊报表查询(&X)")

#         # 帮助菜单
#         help_menu = menu_bar.addMenu("帮助(&H)")

#         # 创建子菜单项
#         # 供应商设置
#         supplier_settings_action = QAction("供应商设置", self)
#         supplier_settings_action.triggered.connect(self.open_supplier_settings)
#         basic_info_settings_menu.addAction(supplier_settings_action)

#         #材料分类设置
#         material_category_settings_action = QAction("材料分类设置", self)
#         material_category_settings_action.triggered.connect(self.open_material_category_settings)
#         basic_info_settings_menu.addAction(material_category_settings_action)

#         #材料属性设置
#         material_attributes_settings_action = QAction("材料属性设置", self)
#         material_attributes_settings_action.triggered.connect(self.open_material_attributes_settings)
#         basic_info_settings_menu.addAction(material_attributes_settings_action)

#         #材料设置
#         material_settings_action = QAction("材料设置", self)
#         material_settings_action.triggered.connect(self.open_material_settings)
#         basic_info_settings_menu.addAction(material_settings_action)

#     def open_material_settings(self):
#         # 打开材料设置对话框
#         dialog = MaterialSettingsDialog(self)
#         dialog.exec_()

#     def open_material_attributes_settings(self):
#         # 打开材料属性设置对话框
#         dialog = MaterialAttributesSettingsDialog(self)
#         dialog.exec_()

#     def open_material_category_settings(self):
#         # 打开材料分类设置对话框
#         dialog = MaterialCategorySettingsDialog(self)
#         dialog.exec_()

#     def open_supplier_settings(self):
#         # 打开供应商设置对话框
#         dialog = SupplierSettingsDialog(self)
#         dialog.exec_()

#     def create_toolbar(self):
#         # 创建工具栏
#         toolbar = QToolBar("Main Toolbar", self)
#         self.addToolBar(toolbar)

#         # 添加工具栏按钮（可扩展性保留）
#         save_action = QAction("保存", self)
#         exit_action = QAction("退出", self)
#         toolbar.addAction(save_action)
#         toolbar.addAction(exit_action)

#     def create_statusbar(self):
#         # 创建状态栏
#         status_bar = QStatusBar()
#         self.setStatusBar(status_bar)

#         # 设置状态栏的初始信息
#         status_bar.showMessage("就绪")

#     def init_ui(self):
#         # 初始化用户界面，保留空白区域以供扩展
#         pass


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = DrugManagementSystem()
#     main_window.show()
#     sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStatusBar, QToolBar, QWidget, QVBoxLayout, QStackedWidget
from supplier_settings_dialog import SupplierSettingsDialog
from material_category_settings_dialog import MaterialCategorySettingsDialog
from material_attributes_settings_dialog import MaterialAttributesSettingsDialog
from material_settings_dialog import MaterialSettingsWidget  # 导入MaterialSettingsWidget

class DrugManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和初始尺寸
        self.setWindowTitle("药物管理系统")
        self.setGeometry(100, 100, 1024, 768)

        # 创建菜单栏
        self.create_menus()

        # 创建工具栏
        self.create_toolbar()

        # 创建状态栏
        self.create_statusbar()

        # 初始化中心窗口区域
        self.init_ui()

    def create_menus(self):
        # 创建菜单栏
        menu_bar = self.menuBar()

        # 系统管理菜单
        system_management_menu = menu_bar.addMenu("系统管理(&S)")

        # 基础信息设置菜单
        basic_info_settings_menu = menu_bar.addMenu("基础信息设置(&B)")

        # 业务信息设置菜单
        business_info_settings_menu = menu_bar.addMenu("业务信息设置(&Y)")

        # 门诊业务菜单
        outpatient_business_menu = menu_bar.addMenu("门诊业务(&M)")

        # 业务管理菜单
        business_management_menu = menu_bar.addMenu("业务管理(&T)")

        # 业务报表查询菜单
        business_report_query_menu = menu_bar.addMenu("业务报表查询(&Q)")

        # 库存报表查询菜单
        inventory_report_query_menu = menu_bar.addMenu("库存报表查询(&R)")

        # 门诊报表查询菜单
        outpatient_report_query_menu = menu_bar.addMenu("门诊报表查询(&X)")

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助(&H)")

        # 创建子菜单项
        # 供应商设置
        supplier_settings_action = QAction("供应商设置", self)
        supplier_settings_action.triggered.connect(self.open_supplier_settings)
        basic_info_settings_menu.addAction(supplier_settings_action)

        # 材料分类设置
        material_category_settings_action = QAction("材料分类设置", self)
        material_category_settings_action.triggered.connect(self.open_material_category_settings)
        basic_info_settings_menu.addAction(material_category_settings_action)

        # 材料属性设置
        material_attributes_settings_action = QAction("材料属性设置", self)
        material_attributes_settings_action.triggered.connect(self.open_material_attributes_settings)
        basic_info_settings_menu.addAction(material_attributes_settings_action)

        # 材料设置
        material_settings_action = QAction("材料设置", self)
        material_settings_action.triggered.connect(self.open_material_settings)
        basic_info_settings_menu.addAction(material_settings_action)

    def open_material_settings(self):
        # 如果材料设置界面尚未创建，则创建它
        if not hasattr(self, 'material_settings_widget'):
            self.material_settings_widget = MaterialSettingsWidget(self)
            self.stacked_widget.addWidget(self.material_settings_widget)

        # 显示材料设置界面
        self.stacked_widget.setCurrentWidget(self.material_settings_widget)

    def open_material_attributes_settings(self):
        # 打开材料属性设置对话框
        dialog = MaterialAttributesSettingsDialog(self)
        dialog.exec_()

    def open_material_category_settings(self):
        # 打开材料分类设置对话框
        dialog = MaterialCategorySettingsDialog(self)
        dialog.exec_()

    def open_supplier_settings(self):
        # 打开供应商设置对话框
        dialog = SupplierSettingsDialog(self)
        dialog.exec_()

    def create_toolbar(self):
        # 创建工具栏
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)

        # 添加工具栏按钮（可扩展性保留）
        save_action = QAction("保存", self)
        exit_action = QAction("退出", self)
        toolbar.addAction(save_action)
        toolbar.addAction(exit_action)

    def create_statusbar(self):
        # 创建状态栏
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # 设置状态栏的初始信息
        status_bar.showMessage("就绪")

    def init_ui(self):
        # 初始化中心窗口区域
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建QVBoxLayout作为中央窗口的布局
        layout = QVBoxLayout(self.central_widget)

        # 创建QStackedWidget用于切换不同的界面
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # 创建一个空白页，用作默认显示的页面
        self.blank_page = QWidget()
        self.stacked_widget.addWidget(self.blank_page)

        # 默认显示空白页
        self.stacked_widget.setCurrentWidget(self.blank_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DrugManagementSystem()
    main_window.show()
    sys.exit(app.exec_())




