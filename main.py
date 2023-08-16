import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QMessageBox
from PyQt5.QtChart import QChart, QChartView, QLineSeries

from lib.industry_fluctuation import PriceCalculation
from correct.neuralprophetclass import PriceForecast
import pandas as pd
import output as op


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.xlsx_file = None
        self.csv_file = None

        self.initUI()

    def initUI(self):
        # 创建组件
        self.btn_upload = QPushButton('上传文件')
        self.btn_calc = QPushButton('开始计算')
        self.text_result = QTextEdit()

        # 创建图表
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_calc)
        layout.addWidget(self.text_result)
        layout.addWidget(self.chart_view)

        self.setLayout(layout)

        # 连接信号槽
        self.btn_upload.clicked.connect(self.file_upload)
        self.btn_calc.clicked.connect(self.start_calc)

    def file_upload(self):
        xlsx_file, _ = QFileDialog.getOpenFileName(self, '选择XLSX文件', '', 'XLSX Files(*.xlsx)')
        csv_file, _ = QFileDialog.getOpenFileName(self, '选择CSV文件', '', 'CSV Files(*.csv)')

        if xlsx_file and csv_file:
            self.xlsx_file = xlsx_file
            self.csv_file = csv_file

    def start_calc(self):
        if self.xlsx_file and self.csv_file:
            forecast_data=op.calculate_price(self.xlsx_file, self.csv_file, 0.32)


            # 绘制价格曲线

            # 预测价格
            forecast = PriceForecast(forecast_data)
            forecast_result = forecast.forecast()
            forecast.print_forecast_points(forecast_result)

        else:
            self.text_result.setText("请先上传文件!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())