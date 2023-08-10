import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# 读取CSV数据
data = pd.read_csv('youe_block_data.csv',encoding="gbk")

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

data['大小'] = data['大小'].apply(convert_size_to_mb)

# 选取所需的列
selected_columns = ['大小', '价格']

# 使用多项式回归拟合数据
x = data['大小'].values.reshape(-1, 1)
y = data['价格'].values

# 设定多项式的阶数，这里设为2
degree = 2
poly = PolynomialFeatures(degree)
x_poly = poly.fit_transform(x)

# 创建并拟合多项式回归模型
model = LinearRegression()
model.fit(x_poly, y)

# 预测
y_pred = model.predict(x_poly)

# 绘制散点图和拟合曲线
# 设置中文字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

# 负号显示样式
plt.rcParams['axes.unicode_minus'] = False
plt.scatter(x, y, color='blue', label='实际数据')
plt.plot(x, y_pred, color='red', label='拟合曲线')
plt.xlabel('大小')
plt.ylabel('价格')
plt.legend()
plt.show()

# 输出回归方程
coefficients = model.coef_
intercept = model.intercept_
print("回归方程：")
print("价格 = ", end="")
for i in range(degree + 1):
    if i == 0:
        print(f"{intercept:.2f}", end=" ")
    else:
        print(f"+ {coefficients[i]:.2f} * (大小 ** {i})", end=" ")
print()
