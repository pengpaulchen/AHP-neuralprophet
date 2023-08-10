import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取CSV文件
csv_file = 'jd_block_data.csv'
df = pd.read_csv(csv_file,encoding="gbk")
# 将大小字段转换为统一的单位（例如MB）
def convert_size_to_mb(size_str):
    if 'KB' in size_str:
        return float(size_str.replace('KB', '')) / 1024
    elif 'MB' in size_str:
        return float(size_str.replace('MB', ''))
    elif 'GB' in size_str:
        return float(size_str.replace('GB', '')) * 1024
    else:
        return 0

df['数据大小'] = df['数据大小'].apply(convert_size_to_mb)
print(df['评分'])
# 选择需要分析的列
columns_to_analyze = ['价格','数据大小']

# 选择这些列的子数据集
selected_data = df[columns_to_analyze]

# 计算关联系数
correlation_matrix = selected_data.corr()

# 打印关联系数
print("关联系数：")
print(correlation_matrix)

# 绘制散点图
# 设置中文字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

# 负号显示样式
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
sns.pairplot(selected_data)
plt.show()

# 绘制热力图
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('特征相关热力图')
plt.show()
# 绘制箱线图
# plt.figure(figsize=(12, 6))
# sns.boxplot(x='商品分类', y='价格', data=df)
# plt.title('不同商品分类下的售价分布')
# plt.xticks(rotation=90)
# plt.show()