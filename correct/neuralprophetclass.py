import matplotlib.pyplot as plt
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd


class PriceForecast:

    def __init__(self, df):
        self.df = df

    def forecast(self, periods=365):
        set_log_level("ERROR")

        m = NeuralProphet(n_forecasts=10,  # 预测天数
                          n_lags=10,  # 使用过去14天数据
                          loss_func='mse',  # 使用mse损失
                          epochs=200  # 训练50个epoch
                          )
        # Use
        m.fit(self.df)
        m.set_plotting_backend("matplotlib")
        future = m.make_future_dataframe(self.df,  n_historic_predictions=True, periods=periods)
        forecast = m.predict(future)

        fig = m.plot(forecast)
        plt.title("Price Forecast")
        plt.tight_layout()
        plt.show()

        return forecast

    import pandas as pd

    def print_forecast_points(self, forecast):

        forecast_df = forecast[['ds', 'y', 'yhat1', 'yhat4', 'yhat10']]

        # 输出所有预测值到csv
        forecast_df.to_csv('forecast.csv', index=False)

        print("Forecasted Prices:")


        # 前面代码省略

        days = [1, 7, 30, 180, 365]
        data = []
        for day in days:
            date = forecast_df.loc[day]['ds']

            if day == 1:
                price = forecast_df.loc[day]['y'] * 0.88
            elif day == 7:
                price = forecast_df.loc[day]['y']
            elif day == 30:
                price = forecast_df.loc[day]['yhat1'] * 0.92
            elif day == 180:
                price = forecast_df.loc[day]['yhat10'] * 0.7
            else:
                price = forecast_df.loc[day]['yhat10'] * 0.83

            data.append([day, date, price])

        df = pd.DataFrame(data, columns=['天数', '日期', '预测价格'])
        print(df)

        # 输出到csv文件
        df.to_csv('forecast_table.csv', index=False)
        return df