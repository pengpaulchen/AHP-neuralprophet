import numpy as np
import pandas as pd
import csv
import re


class DataAnalysis:
    def __init__(self, filename):
        self.filename = filename
        self.score_3rd = []
        self.name_1st = ['数据成本价值', '数据内在价值', '应用场景']
        self.name_2nd = ['数据获取成本', '数据处理成本', '数据质量', '平台建设', '数据安全',
                         '数据产品类型', '群体划分', '关联程度', '市场结构', '所有权水平']
        self.name_3rd = ['与公共管理、服务有关的积淀数据', '外部数据', '私有数据', '加工', '存储', '安全', '维护',
                         '规范性', '完整性', '时效性', '准确性', '精确性', '可访问性', '可信度', '稀缺性',
                         '外部环境', '用户参与', '开发利用', '格式', '协议',
                         '报告', '表格', '图片',
                         '外部', '客户', '内部',
                         '供求', '集中度', '使用方', '来源方']

    def read_data(self):
        with open(self.filename, encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # 跳过第一行
            for row in reader:
                for cell in row[1:]:  # 从第二列开始
                    if re.match(r'^\d+(?:\.\d+)?$', cell):
                        self.score_3rd.append(float(cell))

    def calculate_3rd_weights(self):
        # 三级指标得分处理
        non_null_scores = [s for s in self.score_3rd if s != 0]
        min_score = min(non_null_scores)
        max_score = max(non_null_scores)
        self.score_3rd = [(s - min_score) / (max_score - min_score) if s != 0 else 0 for s in self.score_3rd]

        # 计算三级指标权重
        ε = 0.0001
        p_3rd = (np.array(self.score_3rd) + ε) / (np.sum(self.score_3rd) + len(self.score_3rd) * ε)
        e_3rd = -p_3rd * np.log(p_3rd + ε)
        e_3rd[p_3rd == 0] = 0
        w_3rd = (1 - e_3rd) / np.sum(1 - e_3rd)
        #


        # print("三级指标权重:")
        # for i in range(len(w_3rd)):
        #     print(self.name_3rd[i], w_3rd[i], i)
        return w_3rd

    def calculate_2nd_weights(self, w_3rd):
        # 合并计算二级指标权重
        score_2nd = [np.sum(w_3rd[:3]), np.sum(w_3rd[3:6]), np.sum(w_3rd[6:9]),
                     np.sum(w_3rd[9:12]), np.sum(w_3rd[12:14]), np.sum(w_3rd[14:17]),
                     np.sum(w_3rd[17:20]), np.sum(w_3rd[20:22]), np.sum(w_3rd[22:24]), np.sum(w_3rd[24:26])]

        # 转换为数组
        score_2nd = np.array(score_2nd)

        # 计算二级指标权重
        p_2nd = score_2nd / np.sum(score_2nd)
        e_2nd = -p_2nd * np.log(p_2nd)
        w_2nd = (1 - e_2nd) / np.sum(1 - e_2nd)
        #
        # print("二级指标权重:")
        # for i in range(len(w_2nd)):
        #     print(self.name_2nd[i], w_2nd[i])
        return w_2nd

    def calculate_1st_weights(self, w_2nd):
        # 合并计算一级指标权重
        score_1st = [np.sum(w_2nd[:2]), np.sum(w_2nd[2:5]), np.sum(w_2nd[5:])]

        p_1st = np.array(score_1st) / np.sum(score_1st)
        e_1st = -p_1st * np.log(p_1st)
        w_1st = (1 - e_1st) / np.sum(1 - e_1st)
        #
        # print("一级指标权重:")
        # for i in range(len(w_1st)):
        #     print(self.name_1st[i], w_1st[i])
        return w_1st


# 使用示例
if __name__ == "__main__":
    data_analysis = DataAnalysis('测试数据.csv')
    data_analysis.read_data()
    w_3rd = data_analysis.calculate_3rd_weights()
    w_2nd = data_analysis.calculate_2nd_weights(w_3rd)
    w_1st = data_analysis.calculate_1st_weights(w_2nd)

