
# Volume Analysis with 20-Day Moving Average

This document outlines the steps to analyze trading volume for a stock by comparing the current day's volume to its 20-day Simple Moving Average (SMA).

## Step-by-Step Plan

### 1. Data Acquisition

*   **Objective:** Obtain historical daily stock price and volume data from the PostgreSQL database.
*   **Method:** Use `SQLAlchemy` to connect to the database and load the data into a pandas DataFrame. Ensure your query fetches both the closing price and the volume.
    *   Your `StockPrice` model should include a `volume` column (e.g., `volume = Column(Integer)`).
    *   The query will be similar to the one in `long_term_indices.md`, but you will also use the volume data.

### 2. Volume SMA Calculation

*   **Objective:** Calculate the 20-day SMA of the trading volume.
*   **Method:** Use the `rolling()` function in the pandas library on the volume column.
    *   **Example:**
        ```python
        # Assuming 'data' is your DataFrame with a 'Volume' column
        data['Volume_SMA20'] = data['Volume'].rolling(window=20).mean()
        ```

### 3. Status Determination

*   **Objective:** Compare the most recent trading volume to its 20-day SMA to determine its significance.
*   **Logic:** A common way to gauge significance is to see if the current volume is substantially higher or lower than the average. We can set thresholds for this.
    *   **High Volume:** The current volume is significantly above the 20-day average (e.g., > 150% of the average).
    *   **Low Volume:** The current volume is significantly below the 20-day average (e.g., < 75% of the average).
    *   **Average Volume:** The volume is within a normal range of the average.
*   **Implementation:**
    ```python
    def get_volume_status(current_volume: float, sma20_volume: float) -> str:
        if pd.isna(current_volume) or pd.isna(sma20_volume):
            return "Not enough data"

        # Check if current volume is 50% higher than the average
        if current_volume > (sma20_volume * 1.5):
            return "High Volume"
        # Check if current volume is 25% lower than the average
        elif current_volume < (sma20_volume * 0.75):
            return "Low Volume"
        else:
            return "Average Volume"

    latest_volume = data['Volume'].iloc[-1]
    latest_sma = data['Volume_SMA20'].iloc[-1]
    status = get_volume_status(latest_volume, latest_sma)
    ```

### 4. Generate the Insight

*   **Objective:** Output a clear, human-readable status.
*   **Method:** Based on the analysis, generate one of the following outputs:
    *   "High Volume"
    *   "Low Volume"
    *   "Average Volume"
