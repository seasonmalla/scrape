
# Generating Momentum Insights with Relative Strength Index (RSI)

This document outlines the steps to calculate and interpret the 14-day Relative Strength Index (RSI), a key momentum indicator, for a stock using Python.

## Step-by-Step Plan

### 1. Data Acquisition

*   **Objective:** Obtain historical daily stock price data (closing prices are sufficient) from the PostgreSQL database.
*   **Method:** Use `SQLAlchemy` to connect to the database and load the data into a pandas DataFrame, as detailed in the `long_term_indices.md` guide.

### 2. RSI Calculation

*   **Objective:** Calculate the 14-day RSI.
*   **Method:** The RSI is calculated using the following steps:
    1.  Calculate the price change (delta) from one period to the next.
    2.  Separate the deltas into gains and losses.
    3.  Calculate the average gain and average loss over the 14-day period.
    4.  Calculate the Relative Strength (RS) = Average Gain / Average Loss.
    5.  Calculate the RSI = 100 - (100 / (1 + RS)).
*   **Example (using pandas):**
    ```python
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    # Assuming 'data' is your DataFrame with a 'Close' column
    data['RSI'] = calculate_rsi(data['Close'])
    ```

### 3. Status Determination

*   **Objective:** Determine the momentum status based on the latest RSI value.
*   **Logic:**
    *   **Overbought (RSI > 70):** The stock may be overvalued and could be due for a pullback.
    *   **Oversold (RSI < 30):** The stock may be undervalued and could be due for a bounce.
    *   **Neutral (30 <= RSI <= 70):** The stock is in a neutral zone.
*   **Implementation:**
    ```python
    def get_rsi_status(rsi_value: float) -> str:
        if pd.isna(rsi_value):
            return "Not enough data"
        if rsi_value < 30:
            return "Oversold"
        elif rsi_value > 70:
            return "Overbought"
        else:
            return "Neutral"

    latest_rsi = data['RSI'].iloc[-1]
    status = get_rsi_status(latest_rsi)
    ```

### 4. Generate the Insight

*   **Objective:** Output a clear, human-readable status.
*   **Method:** Based on the analysis, generate one of the following outputs:
    *   "Overbought"
    *   "Oversold"
    *   "Neutral"
