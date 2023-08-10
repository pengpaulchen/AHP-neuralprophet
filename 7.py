from lib import AHPCalculate as ahp, ExcelValueCalculate as evc
import pandas as pd
import datetime
import numpy as np
from fuzzywuzzy import fuzz
import jieba
import zhon.hanzi as zh

class TextSimilarity:
    def __init__(self, industry_data):
        self.industry_data = industry_data
        self.industry_names = self.load_industry_names()

    def load_industry_names(self):
        with open(self.industry_data, 'r', encoding='utf-8') as f:
            industries = f.read().strip().split('、')
        return industries

    def calculate_similarity(self, text1):
        words1 = list(jieba.cut(text1, cut_all=False))
        words1 = [word for word in words1 if word not in zh.punctuation]
        max_similarity = 0
        industry_match = None
        for industry_name in self.industry_names:
            similarity = fuzz.ratio("".join(words1), industry_name)
            if similarity > max_similarity:
                max_similarity = similarity
                industry_match = industry_name
        return industry_match

class PriceCalculation:
    def __init__(self, filename1=None, filename2=None, fluctuation_strength=0.02):
        self.filename1 = filename1
        self.filename2 = filename2
        self.pricing = evc.DynamicExcelPricing(self.filename1, alpha=1.0, beta=10)
        self.final_values = []  # 新增列表存储结果
        self.text_similarity = TextSimilarity(industry_data='industry_data.txt')
        self.fluctuation_strength = fluctuation_strength  # 控制波动强度的参数

    def weight(self):
        data_analysis = ahp.DataAnalysis(self.filename2)
        data_analysis.read_data()
        w_3rd = data_analysis.calculate_3rd_weights()
        w_2nd = data_analysis.calculate_2nd_weights(w_3rd)
        w_1st = data_analysis.calculate_1st_weights(w_2nd)
        return w_1st

    def calculate(self):
        base_price = self.pricing.get_price()
        weight = self.weight()
        output = 0
        impact_factor = (weight[0] + weight[2]) / weight[1]

        # 模拟行业的波动，根据业务需要修改此处的波动函数
        industry_fluctuation = self.simulate_industry_fluctuation()
        output = base_price * impact_factor * industry_fluctuation
        self.final_values.append(output)
        return output

    def simulate_industry_fluctuation(self):
        # 在此处实现模拟行业波动的函数
        industry_name = self.text_similarity.calculate_similarity(self.filename1)
        if industry_name == '经济学':
            return self.economic_fluctuation()
        elif industry_name == '计算机科学与技术':
            return self.cs_technology_fluctuation()
        else:
            return self.default_fluctuation()

    def economic_fluctuation(self):
        # 根据经济学领域的特点设置波动模型
        # 这里使用正弦函数模拟周期变化，但根据数据范围进行缩放，以降低波动范围
        value_range = 5.0  # 数据范围
        fluctuation = value_range * np.sin(2 * np.pi * len(self.final_values) / 50)
        return 1 + self.fluctuation_strength * fluctuation

    def cs_technology_fluctuation(self):
        # 根据计算机科学与技术领域的特点设置波动模型
        # 这里使用正弦函数模拟周期变化，但根据数据范围进行缩放，以降低波动范围
        value_range = 5.0  # 数据范围
        fluctuation = value_range * np.sin(2 * np.pi * len(self.final_values) / 50)
        return 1 + self.fluctuation_strength * fluctuation

    def default_fluctuation(self):
        # 对于其他行业的默认波动模型
        # 这里使用正弦函数模拟周期变化，但根据数据范围进行缩放，以降低波动范围
        value_range = 5.0  # 数据范围
        fluctuation = value_range * np.sin(2 * np.pi * len(self.final_values) / 50)
        return 1 + self.fluctuation_strength * fluctuation

    def update_data(self):
        self.pricing.update_matrix()

# 主程序
def main():
    fluctuation_strength = 0.01  # 调整波动强度参数，越小波动范围越小
    PC = PriceCalculation('有色金属测试数据.xlsx', '测试数据.csv', fluctuation_strength=fluctuation_strength)
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

    final_df.to_csv('final_values.csv', index=False)

if __name__ == "__main__":
    main()
