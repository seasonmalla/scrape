
# Generating Long-Term Trend Insights with Moving Averages

This document outlines the steps to calculate and interpret long-term trend indicators for a stock using Python. The primary indicators used are the 50-day and 200-day Simple Moving Averages (SMAs).

## Step-by-Step Plan

### 1. Data Acquisition

*   **Objective:** Obtain historical daily stock price data (closing prices are sufficient) from a PostgreSQL database.
*   **Method:** Use `SQLAlchemy` to connect to the database and query the data. The results can be loaded into a pandas DataFrame.
    *   **Example:**
        ```python
        from sqlalchemy import create_engine, Column, Integer, String, Date, Float
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.ext.declarative import declarative_base
        import pandas as pd

        # 1. Define your data model (should match your DB table)
        Base = declarative_base()
        class StockPrice(Base):
            __tablename__ = 'stock_prices'
            id = Column(Integer, primary_key=True)
            ticker = Column(String)
            date = Column(Date)
            close = Column(Float)

        # 2. Setup database connection
        DATABASE_URL = "postgresql://user:password@host:port/database"
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # 3. Query the data
        db = SessionLocal()
        query = db.query(StockPrice).filter(StockPrice.ticker == 'AAPL').order_by(StockPrice.date)
        data = pd.read_sql(query.statement, db.bind)
        db.close()

        # Rename columns to match what the rest of the script expects (e.g., 'Close')
        data.rename(columns={'close': 'Close'}, inplace=True)
        # Ensure the 'date' column is the index
        data.set_index('date', inplace=True)
        ```

### 2. Data Preparation

*   **Objective:** Ensure the data is clean and ready for analysis.
*   **Method:**
    *   Handle any missing values (e.g., by filling or removing them).
    *   Ensure the data is sorted by date in ascending order.

### 3. SMA Calculation

*   **Objective:** Calculate the 50-day and 200-day SMAs.
*   **Method:** Use the `rolling()` function in the pandas library.
    *   **Example:**
        ```python
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        data['SMA200'] = data['Close'].rolling(window=200).mean()
        ```

### 4. Trend Analysis & Status Determination

*   **Objective:** Compare the two SMAs to determine the current trend status.
*   **Logic:**
    *   **Golden Cross (Bullish):** The 50-day SMA crosses *above* the 200-day SMA. This is a signal of a potential long-term uptrend.
    *   **Death Cross (Bearish):** The 50-day SMA crosses *below* the 200-day SMA. This is a signal of a potential long-term downtrend.
    *   **Neutral:** The two SMAs are very close to each other or are frequently crossing, indicating a sideways or consolidating market.
*   **Implementation:**
    *   Get the most recent SMA values.
    *   Compare `SMA50` and `SMA200`.
    *   Check for recent crossovers to identify active "Golden Cross" or "Death Cross" conditions.

### 5. Generate the Insight

*   **Objective:** Output a clear, human-readable status.
*   **Method:** Based on the analysis in the previous step, generate one of the following outputs:
    *   "Bullish - Golden Cross active"
    *   "Bearish - Death Cross active"
    *   "Neutral"
