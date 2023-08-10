from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
df = pd.read_csv("final_values.csv")
# m = NeuralProphet()
# metrics = m.fit(df)
# forecast = m.predict(df)
#
#
# fig_forecast = m.plot(forecast)
# fig_components = m.plot_components(forecast)
# fig_model = m.plot_parameters()

#
# m = NeuralProphet().fit(df, freq="D")
# df_future = m.make_future_dataframe(df, periods=30)
# forecast = m.predict(df_future)
# fig_forecast = m.plot(forecast)
import pandas as pd

# Load the dataset from the CSV file using pandas

# Plot the dataset, showing price (y column) over time (ds column)
plt = df.plot(x="ds", y="y", figsize=(15, 5))
# Import the NeuralProphet class


# Disable logging messages unless there is an error
set_log_level("ERROR")

# Create a NeuralProphet model with default parameters
m = NeuralProphet()
# Use static plotly in notebooks
m.set_plotting_backend("plotly")

# Fit the model on the dataset (this might take a bit)haixia2.py
metrics = m.fit(df)
# Create a new dataframe reaching 365 into the future for our forecast, n_historic_predictions also shows historic data
df_future = m.make_future_dataframe(df, n_historic_predictions=True, periods=365)

# Predict the future
forecast = m.predict(df_future)

# Visualize the forecast
m.plot(forecast).show()
