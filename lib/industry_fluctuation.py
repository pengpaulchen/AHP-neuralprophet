import lib.ExcelValueCalculate as evc
from lib import AHPCalculate as ahp
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
    def __init__(self, filename1, filename2,alpha):
        self.filename1 = filename1
        self.filename2 = filename2
        self.alpha=alpha
        self.pricing = evc.DynamicExcelPricing(self.filename1, self.alpha)
        self.final_values = []  # 新增列表存储结果
        self.text_similarity = TextSimilarity(industry_data='./lib/industry_data.txt')

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
        # print(f"文件属于行业：{industry_name}")
        if industry_name == '化工':
            return self.economic_fluctuation()
        elif industry_name == '汽车':
            return self.cs_technology_fluctuation()
        elif industry_name=='隐私':
            return 1000
        elif industry_name=='个人':
            return 1000
        else:
            return self.default_fluctuation()




    def economic_fluctuation(self):
        # 根据经济学领域的特点设置波动模型
        # 这里仅做示例，使用正态分布模拟波动
        return 1 + np.random.normal(0, 0.05)  # 假设波动范围在±5%

    def cs_technology_fluctuation(self):
        # 根据计算机科学与技术领域的特点设置波动模型
        # 这里仅做示例，使用正态分布模拟波动
        return 1 + np.random.normal(0, 0.02)  # 假设波动范围在±2%

    def default_fluctuation(self):
        # 对于其他行业的默认波动模型
        return 1 + np.random.uniform(-0.1, 0.1)  # 假设波动范围在±10%

    def update_data(self):
        self.pricing.update_matrix()

# 主程序
