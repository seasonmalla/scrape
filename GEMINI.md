# Gemini Code Understanding

This document provides a high-level overview of the project, intended to be used by the Gemini model for providing context-aware assistance.

## Project Overview

This project is a Python-based cron job that retrieves financial data from the Nepal Stock Exchange (NEPSE). It is built using the Flask web framework and is designed to be deployed on the Vercel platform.

The primary function of the application is to scrape data from the NEPSE API, process it, and store it in a PostgreSQL database. The application exposes several API endpoints for interacting with the scraped data.

## Key Technologies

*   **Backend:** Python, Flask
*   **Data Scraping:** `nepse` (unofficial NEPSE API library), `httpx`
*   **Database:** PostgreSQL, `SQLAlchemy`, `psycopg2-binary`
*   **Data Processing:** `pandas`
*   **Deployment:** Vercel
*   **Error Tracking:** Rollbar
*   **Environment Management:** `python-dotenv`

## Project Structure

*   `app.py`: The main Flask application file containing the API endpoints and data scraping logic.
*   `requirements.txt`: A list of Python dependencies for the project.
*   `vercel.json`: Configuration file for deploying the application on Vercel.
*   `.env`: (Not present in the repository) Used for storing environment variables such as database credentials and secret keys.

## API Endpoints

The application provides the following API endpoints:

*   `/`: A simple "Hello World!" endpoint.
*   `/api/v1/market_status`: Retrieves the current market status from NEPSE.
*   `/api/v1/financial`: Retrieves financial reports for a given security.
*   `/api/v1/divided`: Retrieves dividend information for a given security.
*   `/api/v1/sector-summary`: Retrieves and saves the sector-wise summary.
*   `/api/v1/scrape`: Scrapes and saves the price and volume history for the current day.
*   `/api/v1/company-list`: Retrieves and saves the list of companies and their sectors.
*   `/api/v1/sector-overview`: Retrieves an overview of all sectors.
*   `/api/v1/market-summary`: Retrieves the market summary.

All API endpoints require a `secret_key_scrape` in the request body for authentication.

## How to Run

1.  Install the required dependencies: `pip install -r requirements.txt`
2.  Set up the environment variables in a `.env` file (see `app.py` for required variables).
3.  Run the Flask application: `python app.py`