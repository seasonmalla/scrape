# Stock Recommendation Engine Strategy (LLM-Powered)

## 1. Objective
To provide users with actionable buy and sell recommendations for stocks traded on the NEPSE, accessed via a credit-based system. The goal is to leverage a hybrid approach, combining robust technical analysis with the nuanced pattern-recognition capabilities of a Large Language Model (LLM).

**Disclaimer:** This strategy is based on technical analysis and AI-generated insights. It is not financial advice. All investment decisions carry risk, and past performance is not indicative of future results. Users should be encouraged to do their own research.

## 2. Core Philosophy: Hybrid "Analyst Summary" Approach
The core philosophy is to **not** feed raw, extensive historical data directly to an LLM. This is inefficient, costly, and prone to misinterpretation of short-term noise.

Instead, we adopt a two-step hybrid model:
1.  **Programmatic Feature Extraction:** Use traditional, proven technical indicators to analyze the full historical data and "compress" it into a set of key, insightful metrics. This step turns raw price data into meaningful concepts (e.g., "long-term trend is bullish").
2.  **LLM for Nuanced Analysis:** Feed these extracted features, formatted as a concise "Analyst Summary," to an LLM. The LLM's role is to weigh the (sometimes conflicting) indicators, incorporate qualitative data (like news), and provide a final, reasoned recommendation, much like a human expert would.

This approach leverages the strengths of both worlds: the mathematical rigor of technical analysis and the sophisticated, context-aware reasoning of LLMs.

## 3. Data Requirements
For each stock, the following daily data points are required:
- **Date**
- **Open**, **High**, **Low**, **Close** prices
- **Volume** traded
- **Company Name**
- **Price Change:** From the previous day.
- **Sector:** The industry sector.
- **Relevant News Snippets** (Optional)

## 4. The LLM-Powered Recommendation Strategy

### Step 1: Pre-computation of Key Indicators (Feature Extraction)
For each stock, a script will run daily to calculate a set of indicators from the historical data. This does **not** involve the LLM.

-   **Long-Term Trend:** 50-day and 200-day Simple Moving Averages (SMA). Determine the status (e.g., "Bullish - Golden Cross active," "Bearish - Death Cross active," "Neutral").
-   **Momentum:** 14-day Relative Strength Index (RSI). Determine the status (e.g., "Oversold," "Overbought," "Neutral").
-   **Volume Analysis:** 20-day Simple Moving Average of Volume. Compare current volume to the average (e.g., "High Volume," "Low Volume").
-   **Recent Performance:** Calculate 1-week and 1-month price percentage changes.
-   **Volatility:** Calculate the 20-day standard deviation of the closing price (Bollinger Bands width could also be used).

### Step 2: Generating the LLM Prompt (The "Analyst Summary")
Combine the pre-computed features for all stocks into a single, structured, token-efficient prompt for the LLM.

**Prompt Template for Batch Processing:**
```
You are an expert stock analyst for the NEPSE market. Your task is to review the provided summaries for various stocks and identify the best potential BUY and SELL opportunities within each sector.

For each stock, you will be given a summary of its technical indicators and recent performance.

Based on this information, provide your recommendations in a single JSON object. The root object should have a single key: `recommendations_by_sector`. This key should contain an array of objects, where each object represents a sector.

Each sector object must have the following structure:
- `sector`: The name of the sector.
- `buy_recommendations`: An array of up to 5 of the strongest BUY recommendations for that sector.
- `sell_recommendations`: An array of up to 5 of the strongest SELL recommendations for that sector.

Each individual recommendation object within the `buy_recommendations` and `sell_recommendations` arrays must have the following structure:
- `ticker`: The stock ticker symbol.
- `company_name`: The full name of the company.
- `signal`: The recommendation signal, either "BUY" or "SELL".
- `date`: The date the signal was generated.
- `current_price`: The latest closing price.
- `change`: The price change from the previous day.
- `reason`: A concise, one-sentence explanation for the recommendation.

Rank the recommendations within each list (buys and sells) with the strongest opportunities first. If a sector has no buy or sell recommendations, the corresponding array should be empty.

Here are the stock summaries for today (2025-06-28):

[
  {
    "ticker": "NABIL",
    "company_name": "Nabil Bank Limited",
    "sector": "Commercial Banks",
    "current_price": 850.00,
    "change": "+10.00 (+1.19%)",
    "long_term_trend": "Bullish, Golden Cross occurred 25 days ago",
    "momentum_rsi": 68,
    "recent_volume": "Strong, 1.5x the 20-day average",
    "recent_performance": "1-week: +4%, 1-month: +9%",
    "volatility": "Moderate",
    "recent_news": "Nabil Bank has announced a strong Q4 profit growth."
  },
  {
    "ticker": "CHCL",
    "company_name": "Chilime Hydropower Company Limited",
    "sector": "Hydropower",
    "current_price": 550.00,
    "change": "-5.00 (-0.90%)",
    "long_term_trend": "Bearish, Death Cross occurred 10 days ago",
    "momentum_rsi": 35,
    "recent_volume": "Below average",
    "recent_performance": "1-week: -2%, 1-month: -7%",
    "volatility": "Low",
    "recent_news": "No significant news."
  }
]

JSON Output:
```

### Step 3: LLM Analysis and Recommendation
The LLM processes the prompt and returns a structured JSON response as specified.


**Example LLM Output:**
```json
{
  "recommendations_by_sector": [
    {
      "sector": "Commercial Banks",
      "buy_recommendations": [
        {
          "ticker": "NABIL",
          "company_name": "Nabil Bank Limited",
          "signal": "BUY",
          "date": "2025-06-28",
          "current_price": 850.00,
          "change": "+10.00 (+1.19%)",
          "reason": "NABIL shows a strong bullish trend with good momentum and positive news, indicating further upside potential."
        }
      ],
      "sell_recommendations": []
    },
    {
      "sector": "Hydropower",
      "buy_recommendations": [],
      "sell_recommendations": [
        {
          "ticker": "CHCL",
          "company_name": "Chilime Hydropower Company Limited",
          "signal": "SELL",
          "date": "2025-06-28",
          "current_price": 550.00,
          "change": "-5.00 (-0.90%)",
          "reason": "CHCL is in a bearish trend with weak momentum and declining performance, a signal to sell."
        }
      ]
    }
  ]
}
```

This output is then parsed by the system. The application's UI will iterate through the `recommendations_by_sector` array to display the recommendations, grouped by sector.

## 5. Credit and Caching System

Access to the daily recommendations is controlled by a credit-based system enforced by the backend API.

-   **Cost:** Viewing the recommendations for the first time on any given day costs **5 credits**.
-   **Credit Deduction:** The backend API is responsible for checking the user's wallet balance and deducting the credits upon a successful request.
-   **Caching:** After the first successful view, the recommendation data for that user and that day is cached. Subsequent requests on the same day will not incur a credit charge and will be served from the cache.
-   **Insufficient Credits:** If a user has fewer than 5 credits, the API will reject the request, likely with an HTTP 402 Payment Required status or a specific error message in the JSON response. The frontend must handle this error gracefully.

## 6. Risk Management
Users should be reminded of standard investment risks, including the principles of position sizing and diversification.

## 6. Implementation Notes
1.  **Data Processing Script:** Create a robust script (e.g., in Python with `pandas` and `pandas_ta`) to perform the daily feature extraction for all stocks. This script must include the stock's sector.
2.  **LLM Integration:** Use an API to send the generated prompts to your chosen LLM and parse the structured JSON response.
3.  **UI Implementation:** The frontend application will be responsible for:
    -   Displaying the locked state with the "View Recommendations" button.
    -   Making the API call to fetch recommendations when the button is clicked.
    -   Handling the "insufficient credits" error from the API.
    -   If successful, parsing the `recommendations_by_sector` array and displaying the data.
4.  **Prompt Engineering:** The quality of the recommendation heavily depends on the prompt. It may require significant refinement and backtesting to find the most effective structure and wording for optimal results.
5.  **Backtesting:** A good approach is to save the generated "Analyst Summaries" for each day historically. Then, you can run these historical summaries through the LLM to simulate its past decisions and evaluate the hypothetical performance of the strategy.
6.  **Cost Management:** This hybrid approach is highly cost-effective, but it's still important to monitor LLM API usage.
