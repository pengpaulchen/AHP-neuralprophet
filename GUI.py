import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget)

from lib.AHPCalculate import DataAnalysis
from lib.ExcelValueCalculate import DynamicExcelPricing
import pandas as pd


class MyGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        # 初始化界面、组件
        self.setWindowTitle("Data File GUI")
        self.data_file_label = QLabel("No data file selected")
        self.config_file_label = QLabel("No config file selected")
        self.select_data_btn = QPushButton("Select Data File")
        self.select_config_btn = QPushButton("Select Config File")
        self.run_btn = QPushButton("Run")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.data_file_label)
        layout.addWidget(self.select_data_btn)
        layout.addWidget(self.config_file_label)
        layout.addWidget(self.select_config_btn)
        layout.addWidget(self.run_btn)

        # 设置布局
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # 按钮点击信号连接槽函数
        self.select_data_btn.clicked.connect(self.select_data_file)
        self.select_config_btn.clicked.connect(self.select_config_file)
        self.run_btn.clicked.connect(self.run)

    def select_data_file(self):
        # 选择数据文件逻辑
        fname = QFileDialog.getOpenFileName(self, 'Open DATA file')
        if fname[0]:
            self.data_file_label.setText(fname[0])

    def select_config_file(self):
        # 选择配置文件逻辑
        fname = QFileDialog.getOpenFileName(self, 'Open CONFIG file')
        if fname[0]:
            self.config_file_label.setText(fname[0])

    def run(self):
        try:
            # 读取上传的Excel文件
            data_file = self.data_file_label.text()
            if not data_file:
                raise Exception('No data file selected!')

            df = pd.read_excel(data_file)

            # 读取权重计算配置文件
            config_file = self.config_file_label.text()
            if not config_file:
                result = 1.0  # 没有配置文件,结果为1
            else:
                weights = DataAnalysis(config_file)
                weights.read_data()
                w_3rd = weights.calculate_3rd_weights()
                w_2nd = weights.calculate_2nd_weights(w_3rd)
                w_1st = weights.calculate_1st_weights(w_2nd)

            # 创建定价实例
            pricing = DynamicExcelPricing(data_file,alpha=0.3)

            # 计算结果
            results = []
            for i in range(100):
                price = pricing.get_price()


                if config_file:
                    impact_factor = (w_1st[0] + w_1st[2]) / w_1st[1]
                    result = price * impact_factor
                else:
                    result = price

                results.append(result)
                pricing.update_matrix()

            # 显示结果
            QMessageBox.information(self, 'Results', str(results))

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


app = QApplication(sys.argv)
window = MyGUI()
window.show()
app.exec_()