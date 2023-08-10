from lib import AHPCalculate as ahp, ExcelValueCalculate as evc
import pandas as pd
import datetime
class PriceCalculation:
    def __init__(self, filename1=None, filename2=None):
        self.filename1 = filename1
        self.filename2 = filename2
        self.pricing = evc.DynamicExcelPricing(self.filename1, alpha=0.4)
        self.final_values = []  # 新增列表存储结果
    def weight(self):
        data_analysis= ahp.DataAnalysis(self.filename2)
        data_analysis.read_data()
        w_3rd = data_analysis.calculate_3rd_weights()
        w_2nd = data_analysis.calculate_2nd_weights(w_3rd)
        w_1st = data_analysis.calculate_1st_weights(w_2nd)
        return w_1st

    def calculate(self):
        base_price = self.pricing.get_price()
        weight=self.weight()
        output = 0
        impact_factor = (weight[0]+weight[2])/weight[1]
        output = base_price * impact_factor
        self.final_values.append(output)
        return output

    def update_data(self):

        self.pricing.update_matrix()
PC=PriceCalculation('有色金属测试数据.xlsx','测试数据.csv')
PC.weight()
for i in range(50):

    finalValue = PC.calculate()
    PC.update_data()
    if i == 0:
        continue
    else:
        print(finalValue)

PC.final_values.pop(0)
final_df = pd.DataFrame(PC.final_values, columns=['y'])
start_date = datetime.datetime(2023, 1, 1)
dates = [start_date + datetime.timedelta(days=i) for i in range(len(PC.final_values))]
final_df['ds'] = dates

final_df.to_csv('D:\code\python\neuralprophet\final_values.csv', index=False)