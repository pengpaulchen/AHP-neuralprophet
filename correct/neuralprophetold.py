from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
df = pd.read_csv("final_values.csv")

df['y'] = df['y'].rolling(window=7, center=True).mean()
# Load the dataset from the CSV file using pandas

# Plot the dataset, showing price (y column) over time (ds column)
plt = df.plot(x="ds", y="y", figsize=(15, 5))
# Import the NeuralProphet class


# Disable logging messages unless there is an error
set_log_level("ERROR")

# Create a NeuralProphet model wi../......././+++++----+++------++++++++------+----th default parameters
m = NeuralProphet( n_forecasts=30, # 预测天数
    n_lags=30,   # 使用过去14天数据
    loss_func='mse', # 使用mse损失
    epochs=200 # 训练50个epoch
 )
# Use static plotly in notebooks
m.set_plotting_backend("plotly")

# Fit the model on the dataset (this might take a bit)
metrics = m.fit(df)
# Create a new dataframe reaching 365 into the future for our forecast, n_historic_predictions also shows historic data
df_future = m.make_future_dataframe(df, n_historic_predictions=True, periods=365)

# Predict the future
forecast = m.predict(df_future)
print(forecast)

# Visualize the forecast
m.plot(forecast).show()
