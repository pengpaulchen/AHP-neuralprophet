from lib.industry_fluctuation import PriceCalculation
import pandas as pd
import datetime

def main():
    PC = PriceCalculation('lib/有色金属测试数据.xlsx', 'lib/测试数据.csv')
    PC.weight()
    for i in range(5):
        finalValue = PC.calculate()
        PC.update_data()
        if i == 0:
            continue
        else:
            print(round(finalValue,2))

    PC.final_values.pop(0)
    PC.final_values.pop(1)
    PC.final_values.pop(2)
    final_df = pd.DataFrame(PC.final_values, columns=['y'])
    start_date = datetime.datetime(2023, 1, 1)
    dates = [start_date + datetime.timedelta(days=i) for i in range(len(PC.final_values))]
    final_df['ds'] = dates

    final_df.to_csv('./correct/final_values.csv', index=False)

if __name__ == "__main__":
    main()
