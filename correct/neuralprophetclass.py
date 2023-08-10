import matplotlib.pyplot as plt
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd


class PriceForecast:

    def __init__(self, df):
        self.df = df

    def forecast(self, periods=365):
        set_log_level("ERROR")

        m = NeuralProphet(
            n_forecasts=10,
            n_lags=20
        )

        m.fit(self.df)

        future = m.make_future_dataframe(self.df, periods=periods)
        forecast = m.predict(future)

        fig = m.plot(forecast)
        plt.title("Price Forecast")
        plt.show()

        return forecast

    def print_forecast_points(self, forecast, days=None):
        if days is None:
            days = [1, 7, 30, 180, 359]
        print("Forecasted Prices:")
        print(len(forecast))
        for day in days:
            date = forecast.loc[day]['ds']
            price = forecast.loc[day]['yhat1']
            print(f"Day {day} ({date}): {round(price, 2)}")