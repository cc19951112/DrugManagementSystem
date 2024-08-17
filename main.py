import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStatusBar, QToolBar
from supplier_settings_dialog import SupplierSettingsDialog  # 导入供应商设置对话框类

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

        # 初始化UI
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
        # 初始化用户界面，保留空白区域以供扩展
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DrugManagementSystem()
    main_window.show()
    sys.exit(app.exec_())
