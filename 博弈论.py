import random
import matplotlib.pyplot as plt
import pandas as pd

# 读取final_value序列
final_df = pd.read_csv('final_values.csv')

# 存储结果
supplier_profits = []
demander_profits = []

# 参数设置
COST_ACCURATE = 8
COST_INACCURATE = 5
PENALTY = 20


# 数据供应方随机选择概率
def supplier_prob():
    return random.uniform(0.6, 0.9)


# 数据需求方随机选择概率
def demander_prob():
    return random.uniform(0.5, 1)


# 数据供应方选择
def supplier_choice(prob):
    r = random.random()
    if r < prob:
        return 'accurate'
    else:
        return 'inaccurate'


# 数据需求方选择
def demander_choice(prob):
    r = random.random()
    if r < prob:
        return 'buy'
    else:
        return 'not_buy'

# 单次模拟
def one_trade():
    # 更新VALUE
    global VALUE
    VALUE = final_df['y'].iloc[-1]

    prob_supply = supplier_prob()
    prob_demand = demander_prob()

    supplier = supplier_choice(prob_supply)
    demander = demander_choice(prob_demand)

    if supplier == 'accurate':
        if demander == 'buy':
            supplier_profit = VALUE - COST_ACCURATE
            demander_profit = VALUE
        else:
            supplier_profit = -COST_ACCURATE
            demander_profit = 0

    else:
        if demander == 'buy':
            supplier_profit = VALUE - COST_INACCURATE - PENALTY
            demander_profit = -VALUE
        else:
            supplier_profit = -COST_INACCURATE
            demander_profit = 0

    return supplier_profit, demander_profit


# 多次模拟
times = 100
for i in range(times):
    profit1, profit2 = one_trade()

    # 更新VALUE
    VALUE = final_df['y'].iloc[-1]

    supplier_profits.append(profit1)
    demander_profits.append(profit2)

# 绘图
# 折线图
plt.plot(supplier_profits, color='b', label='Supplier')
plt.plot(demander_profits, color='r', label='Demander')
plt.title("Profits Comparison")
plt.xlabel("Round")
plt.ylabel("Profit")
plt.legend()
plt.show()

# 直方图
plt.hist(supplier_profits, color='b', alpha=0.5, label='Supplier')
plt.hist(demander_profits, color='r', alpha=0.5, label='Demander')
plt.title("Profit Distribution")
plt.xlabel("Profit")
plt.ylabel("Frequency")
plt.legend()
plt.show()