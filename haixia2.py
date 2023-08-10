import pandas as pd
from neuralprophet import NeuralProphet, set_log_level
import matplotlib.pyplot as plt

# Disable logging messages unless there is an error
set_log_level("ERROR")

# Load the dataset from the CSV file using pandas
df = pd.read_csv("final_values.csv")
print(df)

from statsmodels.graphics.tsaplots import plot_acf

fig = plot_acf(df['y'], lags=30)
plt.show()
# Model and prediction
m = NeuralProphet(
    # Disable trend changepoints
    n_changepoints=10,
    # Disable seasonality components
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=True,
    # Add the autogression
    n_lags=20,
    n_forecasts=20
)
m.set_plotting_backend("matplotlib")  # Use matplotlib due to #1235
metrics = m.fit(df)
print(metrics)
df_future = m.make_future_dataframe(df, n_historic_predictions=True, periods=100)
print(df_future)
forecast = m.predict(df_future)
fig1 = m.plot(forecast)
plt.show()
forecast.to_csv("1.csv")
df_residuals = pd.DataFrame({"ds": df["ds"], "yhat1": df['y'] - forecast["yhat1"]})

fig2 = df_residuals.plot(x="ds", y='yhat1', figsize=(10, 6))
plt.show()
