
# Bollinger Bands Analysis

This document outlines the steps to calculate and interpret Bollinger Bands, a popular technical analysis indicator used to measure market volatility and identify overbought or oversold conditions.

## Step-by-Step Plan

### 1. Data Acquisition

*   **Objective:** Obtain at least 20 days of historical daily stock price data (specifically closing prices) from the PostgreSQL database.
*   **Method:** Use `SQLAlchemy` to connect to the database and load the data into a pandas DataFrame, ensuring it is sorted by date in ascending order. This process is similar to the data acquisition described in `volatility.md`.

### 2. Bollinger Bands Calculation

*   **Objective:** Calculate the Middle Band, Upper Band, and Lower Band of the Bollinger Bands.
*   **Parameters:**
    *   **Period:** Typically 20 days (for the Simple Moving Average and Standard Deviation).
    *   **Standard Deviations:** Typically 2 (for the multiplier of the standard deviation).
*   **Formulas:**
    *   **Middle Band (MB):** 20-day Simple Moving Average (SMA) of the closing price.
    *   **Upper Band (UB):** Middle Band + (2 * 20-day Standard Deviation of closing price).
    *   **Lower Band (LB):** Middle Band - (2 * 20-day Standard Deviation of closing price).
*   **Implementation:**
    ```python
    import pandas as pd

    def calculate_bollinger_bands(prices: pd.Series, window: int = 20, num_std_dev: int = 2) -> pd.DataFrame:
        """
        Calculates Bollinger Bands for a given price series.

        Args:
            prices: A pandas Series of closing prices.
            window: The rolling window period for SMA and StdDev (default is 20).
            num_std_dev: The number of standard deviations for the bands (default is 2).

        Returns:
            A pandas DataFrame with 'Middle_Band', 'Upper_Band', and 'Lower_Band'.
        """
        if not isinstance(prices, pd.Series):
            raise TypeError("Input 'prices' must be a pandas Series.")

        # Calculate Middle Band (20-day SMA)
        middle_band = prices.rolling(window=window).mean()

        # Calculate 20-day Standard Deviation
        std_dev = prices.rolling(window=window).std()

        # Calculate Upper and Lower Bands
        upper_band = middle_band + (std_dev * num_std_dev)
        lower_band = middle_band - (std_dev * num_std_dev)

        bollinger_bands = pd.DataFrame({
            'Middle_Band': middle_band,
            'Upper_Band': upper_band,
            'Lower_Band': lower_band
        })
        return bollinger_bands

    # Assuming 'data' is your DataFrame with a 'Close' column
    price_series = data['Close']
    bb_df = calculate_bollinger_bands(price_series)
    ```

### 3. Interpretation

*   **Objective:** Interpret the Bollinger Bands to understand volatility and potential trading signals.
*   **Logic:**
    *   **Band Width:**
        *   **Widening Bands:** Indicate increasing volatility.
        *   **Narrowing Bands (Squeeze):** Indicate decreasing volatility, often preceding a period of increased volatility.
    *   **Price Action Relative to Bands:**
        *   **Price near Upper Band:** May suggest the stock is overbought or reaching resistance. A close above the upper band can indicate strong momentum.
        *   **Price near Lower Band:** May suggest the stock is oversold or reaching support. A close below the lower band can indicate strong selling pressure.
        *   **Price crossing Middle Band:** Can be used as a trend indicator. Price crossing above the middle band may signal an uptrend, while crossing below may signal a downtrend.
*   **Implementation (Conceptual Status Determination):**
    ```python
    # Get the latest values
    latest_price = price_series.iloc[-1]
    latest_middle_band = bb_df['Middle_Band'].iloc[-1]
    latest_upper_band = bb_df['Upper_Band'].iloc[-1]
    latest_lower_band = bb_df['Lower_Band'].iloc[-1]

    status = "Neutral"
    if latest_price > latest_upper_band:
        status = "Price is above Upper Band (Potentially Overbought/Strong Uptrend)"
    elif latest_price < latest_lower_band:
        status = "Price is below Lower Band (Potentially Oversold/Strong Downtrend)"
    elif latest_price > latest_middle_band:
        status = "Price is above Middle Band (Uptrend Bias)"
    elif latest_price < latest_middle_band:
        status = "Price is below Middle Band (Downtrend Bias)"

    # You can also analyze band width for volatility changes
    band_width = latest_upper_band - latest_lower_band
    # Compare band_width to historical average band_width to determine if it's wide or narrow
    ```

### 4. Generate the Insight

*   **Objective:** Output the calculated Bollinger Band values and an interpretation of the current price action relative to the bands.
*   **Method:** Present the values and status in a clear, readable format.
