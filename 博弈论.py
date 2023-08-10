import random
from lib import AHPCalculate as ahp, ExcelValueCalculate as evc

# 调用你的代码获取参数
pricing = evc.DynamicExcelPricing('lib/有色金属测试数据.xlsx', alpha=0.3)
base_price = pricing.get_price()

data_analysis = ahp.DataAnalysis('lib/测试数据.csv')
data_analysis.read_data()
w_3rd = data_analysis.calculate_3rd_weights()
w_2nd = data_analysis.calculate_2nd_weights(w_3rd)
w_1st = data_analysis.calculate_1st_weights(w_2nd)
impact_factor = (w_1st[0] + w_1st[2]) / w_1st[1]

VALUE = base_price * impact_factor  # 数据价值

# 定义参数
ACCURATE_PROB = 0.8  # 数据供应方提供准确数据的概率
INACCURATE_PROB = 0.2  # 数据供应方提供不准确数据的概率
BUY_PROB = 0.7  # 数据需求方购买数据的概率

COST_ACCURATE = w_1st[0]*base_price # 提供准确数据的成本
COST_INACCURATE = w_1st[0]*base_price*0.2  # 提供不准确数据的成本
PENALTY =  5*base_price  # 提供不准确数据的惩罚，假一赔五


# 模拟数据供应方选择


def one_trade():
    def supplier_choice():
        choice = random.random()
        if choice < ACCURATE_PROB:
            return 'accurate'
        else:
            return 'inaccurate'

    # 模拟数据需求方选择
    def demander_choice():
        choice = random.random()
        if choice < BUY_PROB:
            return 'buy'
        else:
            return 'not_buy'

    # 单次交易模拟

    supplier_choice = supplier_choice() # 调用外部函数
    demander_choice = demander_choice()

    supplier_profit = 0
    demander_profit = 0

    if supplier_choice == 'accurate':
        if demander_choice == 'buy':
            demander_profit = VALUE
            supplier_profit = VALUE - COST_ACCURATE
        else:
            supplier_profit = -COST_ACCURATE

    else:
        if demander_choice == 'buy':
            demander_profit = -VALUE
            supplier_profit = VALUE - COST_INACCURATE - PENALTY
        else:
            supplier_profit = -COST_INACCURATE

    return supplier_profit, demander_profit


# 多次交易模拟
def simulate(times):
    total_supplier_profit = 0
    total_demander_profit = 0

    for i in range(times):
        supplier_profit, demander_profit = one_trade()
        total_supplier_profit += supplier_profit
        total_demander_profit += demander_profit

    average_supplier_profit = total_supplier_profit / times
    average_demander_profit = total_demander_profit / times

    print(f'Supplier average profit: {average_supplier_profit}')
    print(f'Demander average profit: {average_demander_profit}')


# 运行模拟
simulate(10000)
