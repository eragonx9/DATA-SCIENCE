import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
from enum import Enum

# Define order states using Enum
class Order(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0

# Configure plot style
plt.style.use("dark_background")

# Parameters for moving averages
short_window = 50
long_window = 200

# Define the date range for data
start_date = dt.datetime.now() - dt.timedelta(days=5 * 365)
end_date = dt.datetime.now()

# Stock ticker symbol
ticker = 'AAPL'

# Fetch historical stock data
data = yf.download(ticker, start_date, end_date)

# Calculate moving averages
data[f'SMA_{short_window}'] = data['Adj Close'].rolling(window=short_window).mean()
data[f'SMA_{long_window}'] = data['Adj Close'].rolling(window=long_window).mean()

# Trim the data to avoid NaN values from rolling calculation
data = data.iloc[long_window:]

# Initialize buy/sell signals and the current state
buy_signals, sell_signals = [], []
current_state = Order.HOLD

# Identify buy and sell signals
for i in range(len(data)):
    short_ma = data[f'SMA_{short_window}'].iloc[i]
    long_ma = data[f'SMA_{long_window}'].iloc[i]
    adj_close = data['Adj Close'].iloc[i]
    
    if short_ma > long_ma and current_state != Order.BUY:
        buy_signals.append(adj_close)
        sell_signals.append(float('nan'))
        current_state = Order.BUY
    elif short_ma < long_ma and current_state != Order.SELL:
        buy_signals.append(float('nan'))
        sell_signals.append(adj_close)
        current_state = Order.SELL
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))

# Add signals to the dataset
data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals

# Display the processed data
print(data)

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data['Adj Close'], label="Share Price", alpha=0.5)
plt.plot(data[f'SMA_{short_window}'], label=f"SMA {short_window}", color="red", linestyle="--")
plt.plot(data[f'SMA_{long_window}'], label=f"SMA {long_window}", color="blue", linestyle="--")
plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="green", lw=3)
plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="red", lw=3)
plt.legend(loc="upper left")
plt.title(f"{ticker} Moving Average Crossover Strategy")
plt.show()
