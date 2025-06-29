
# Recent Performance Analysis

This document outlines the steps to calculate the recent performance of a stock by measuring its price percentage change over 1-week and 1-month periods.

## Step-by-Step Plan

### 1. Data Acquisition

*   **Objective:** Obtain at least one month of historical daily stock price data from the PostgreSQL database.
*   **Method:** Use `SQLAlchemy` to connect to the database and load the data into a pandas DataFrame. Ensure the data is sorted by date in ascending order.

### 2. Performance Calculation

*   **Objective:** Calculate the percentage change in price over the last week (5 trading days) and the last month (21 trading days).
*   **Method:** Use the `pct_change()` method in pandas, which is ideal for this calculation.
*   **Implementation:**
    ```python
    import pandas as pd

    def calculate_performance(prices: pd.Series) -> dict:
        """
        Calculates the 1-week and 1-month price percentage change.

        Args:
            prices: A pandas Series of closing prices, sorted by date.

        Returns:
            A dictionary containing the performance metrics.
        """
        if not isinstance(prices, pd.Series):
            raise TypeError("Input 'prices' must be a pandas Series.")

        performance = {}

        # Calculate 1-Week (5 trading days) performance
        if len(prices) > 5:
            # pct_change(5) calculates the change over 5 periods
            week_change = prices.pct_change(periods=5).iloc[-1]
            performance['1-Week Change'] = f"{week_change * 100:.2f}%"
        else:
            performance['1-Week Change'] = "Not enough data"

        # Calculate 1-Month (21 trading days) performance
        if len(prices) > 21:
            month_change = prices.pct_change(periods=21).iloc[-1]
            performance['1-Month Change'] = f"{month_change * 100:.2f}%"
        else:
            performance['1-Month Change'] = "Not enough data"

        return performance

    # Assuming 'data' is your DataFrame with a 'Close' column
    # Make sure it is sorted by date!
    price_series = data['Close']
    performance_metrics = calculate_performance(price_series)
    ```

### 3. Generate the Insight

*   **Objective:** Output the calculated performance metrics.
*   **Method:** Present the percentage changes in a clear, readable format.
*   **Example Output:**
    ```
    {
        "1-Week Change": "3.45%",
        "1-Month Change": "-1.20%"
    }
    ```
