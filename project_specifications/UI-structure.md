# UI Structure for Stock Recommendation Engine

This document outlines the user interface structure for the stock recommendation feature, designed to be intuitive, informative, and transparent, based on the strategy defined in `recommend.md`.

## 1. Recommendations Page

This page is the entry point for users to access daily stock recommendations. Access is controlled by a credit system.

### 1.1. Initial View / Locked State

When the user first navigates to the page, they will see a locked view.

**Components:**

-   **Wallet Balance Display:** A clearly visible component showing the user's current credit balance, sourced from the existing `wallet-store` (e.g., "Your Credits: 50").
-   **Unlock Button:** A prominent button at the center of the page.
    -   **Text:** "View Today's Recommendations (5 Credits)"
-   **Informational Text:** A brief explanation below the button.
    -   *"Unlock today's AI-powered stock recommendations. The 5-credit fee will be deducted from your wallet. You will have access for the rest of the day."*
-   **Disclaimer Notice:** A brief, non-intrusive banner at the top or bottom.
    -   *"Trading involves risk. These are not financial advice. Always do your own research."* `[Learn More]` (links to the full disclaimer/strategy page).

**State Management & Error Handling:**

-   The component will subscribe to the `wallet-store` to get the user's current credit balance.
-   If the balance is fewer than 5 credits, the "Unlock Button" should be disabled. The UI should reactively update if the store's credit value changes.
-   Clicking the button triggers the API call. If the backend returns an insufficient credits error (e.g., if the store was out of sync), the UI should display a notification and prompt the user to top up their wallet.

### 1.2. Unlocked View

After a user with sufficient credits clicks the unlock button, the view is replaced with the recommendations.

**Components:**

-   **Filters:** A filter section at the top with options for:
    -   **Signal Type:** `[ All ]` (Default), `[ BUY ]`, `[ SELL ]`
    -   **Sector Select:** A dropdown to filter by industry sector (e.g., "Commercial Banks", "Technology", "Hydropower").

-   **Recommendation List:** A scrollable list of stocks, grouped by sector. Each sector will display a maximum of 5 recommendations based on the selected filters. Each item in the list will be a **Recommendation Card**.

### 1.3. Recommendation Card (Component)

Each card represents a single stock recommendation.

-   **Layout:**

    ```
    +----------------------------------------------------+
    | [Stock Ticker] | [Signal]      | [Date]             |
    | [Company Name] |               |                    |
    |----------------------------------------------------|
    | Current Price: [Price] | Change: [+X.XX%]          |
    |                                                    |
    | Reason: [Brief, high-level reason]   [Details ->]  |
    +----------------------------------------------------+
    ```

-   **Fields:**
    -   **Stock Ticker:** e.g., `NABIL`
    -   **Company Name:** e.g., `Nabil Bank Limited`
    -   **Signal:** A colored badge: `BUY` (Green), `SELL` (Red).
    -   **Date:** Date the signal was generated (e.g., `2025-06-27`).
    -   **Current Price:** The latest closing price.
    -   **Change:** Price change from the previous day.
    -   **Reason:** A concise summary of the signal.
    -   **Details Link:** The entire card should be clickable, navigating to `/analyze/[Stock Ticker]` for detailed analysis.

**Example Backend API Output:**
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

## 2. Education & Disclaimer Page

Linked from the `[Learn More]` button. This page ensures transparency.

**Components:**

-   **Full Disclaimer:** The complete legal disclaimer from `recommend.md`.
-   **Our Strategy Explained:** A user-friendly explanation of the concepts:
    -   What is a Simple Moving Average (SMA)?
    -   What is the Golden Cross / Death Cross?
    -   What is the Relative Strength Index (RSI)?
    -   How do we use Volume to confirm a trend?
-   **Risk Management:** The full risk management section from `recommend.md` (Position Sizing, Diversification, etc.).

## 3. (Optional) User Watchlist / Portfolio

A separate tab where users can add stocks they are interested in. The UI would be a list similar to the main dashboard but filtered to only show stocks on their watchlist, displaying the current signal (`BUY` or `SELL`) for each.