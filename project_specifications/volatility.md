
# Volatility Analysis

This document outlines the steps to calculate the volatility of a stock using the 20-day standard deviation of its closing prices. This metric helps in understanding the magnitude of a stock's price fluctuations.

## Step-by-Step Plan

### 1. Data Acquisition

*   **Objective:** Obtain at least 20 days of historical daily stock price data from the PostgreSQL database.
*   **Method:** Use `SQLAlchemy` to connect to the database and load the data into a pandas DataFrame, ensuring it is sorted by date in ascending order.

### 2. Volatility Calculation

*   **Objective:** Calculate the 20-day rolling standard deviation of the closing prices.
*   **Method:** Use the `rolling()` function combined with the `std()` function in the pandas library.
*   **Implementation:**
    ```python
    import pandas as pd

    def calculate_volatility(prices: pd.Series, period: int = 20) -> float:
        """
        Calculates the rolling standard deviation of prices.

        Args:
            prices: A pandas Series of closing prices, sorted by date.
            period: The rolling window period (default is 20).

        Returns:
            The latest volatility value.
        """
        if not isinstance(prices, pd.Series):
            raise TypeError("Input 'prices' must be a pandas Series.")

        if len(prices) < period:
            return None # Not enough data

        # Calculate the 20-day rolling standard deviation
        volatility = prices.rolling(window=period).std().iloc[-1]
        return volatility

    # Assuming 'data' is your DataFrame with a 'Close' column
    price_series = data['Close']
    volatility_value = calculate_volatility(price_series)
    ```

*   **Alternative Method (Bollinger Bands):** Volatility is a core component of Bollinger Bands. The distance between the upper and lower bands is determined by the standard deviation. The width of the bands (Upper Band - Lower Band) is a direct visualization of volatility. A widening of the bands indicates increasing volatility, while a narrowing indicates decreasing volatility.

### 3. Generate the Insight

*   **Objective:** Output the calculated volatility metric.
*   **Method:** The raw standard deviation value represents the typical price fluctuation in the currency of the stock (e.g., USD). To make it more comparable across different stocks, it can be expressed as a percentage of the current price.
*   **Example Output:**
    ```python
    latest_price = price_series.iloc[-1]

    if volatility_value is not None:
        # As a percentage of the current price
        volatility_percentage = (volatility_value / latest_price) * 100
        print(f"20-Day Volatility (Standard Deviation): {volatility_value:.2f}")
        print(f"Volatility as % of Price: {volatility_percentage:.2f}%")
    else:
        print("Not enough data to calculate volatility.")

    ```
