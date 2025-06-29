-- Create users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    google_id VARCHAR(255) NOT NULL,
    has_access BOOLEAN DEFAULT FALSE,
    credits INTEGER DEFAULT 0,
    CONSTRAINT email_unique UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS stock_prices (
        business_date DATE NOT NULL,
        security_id BIGINT NOT NULL,
        symbol VARCHAR(20) NOT NULL,
        security_name VARCHAR(100) NOT NULL,
        open_price NUMERIC(20, 2),
        high_price NUMERIC(20, 2),
        low_price NUMERIC(20, 2),
        close_price NUMERIC(20, 2),
        total_traded_quantity NUMERIC(20, 2),
        total_traded_value NUMERIC(20, 2),
        previous_day_close_price NUMERIC(20, 2),
        fifty_two_week_high NUMERIC(20, 2),
        fifty_two_week_low NUMERIC(20, 2),
        last_updated_time TIMESTAMP,
        last_updated_price NUMERIC(20, 2),
        total_trades NUMERIC(20, 2),
        average_traded_price NUMERIC(20, 2),
        market_capitalization NUMERIC(20, 2),
        CONSTRAINT unique_stock_date UNIQUE (security_id, business_date)
    );

CREATE INDEX IF NOT EXISTS idx_stock_prices_symbol ON stock_prices(symbol);
CREATE INDEX IF NOT EXISTS idx_stock_prices_business_date ON stock_prices(business_date);


CREATE TABLE user_tokens (
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


-- Add Admin User
INSERT INTO users (email, google_id, has_access, credits)
VALUES ('techservicesalliance@gmail.com', 'admin', true, 999999);


-- Create wallets table
CREATE TABLE wallets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    wallet_type VARCHAR(20) NOT NULL CHECK (wallet_type IN ('esewa', 'khalti', 'system')),
    balance INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_user_wallet UNIQUE (user_id, wallet_type)
);

-- Create topup_history table
CREATE TABLE topup_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    wallet_id BIGINT REFERENCES wallets(id),
    operator VARCHAR(20) NOT NULL,
    amount INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    invoice_number VARCHAR(50),
    admin_id BIGINT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Stock Dividends Table
CREATE TABLE stock_dividends (
    id BIGSERIAL PRIMARY KEY,
    security_id INTEGER,
    cash_dividend NUMERIC(20,2),
    bonus_share NUMERIC(20,2),
    right_share NUMERIC(20,2),
    financial_year VARCHAR(50),
    publish_date TIMESTAMP WITHOUT TIME ZONE,
    approved_date TIMESTAMP WITHOUT TIME ZONE,
    data_hash TEXT,
    CONSTRAINT stock_dividends_data_hash_key UNIQUE (data_hash)
);

-- Stock Financials Table
CREATE TABLE stock_financials (
    id BIGSERIAL PRIMARY KEY,
    security_id BIGINT NOT NULL,
    pe_value NUMERIC(20,2) NOT NULL,
    eps_value NUMERIC(20,2) NOT NULL,
    networth_per_share NUMERIC(20,2),
    quarter_name VARCHAR(20) NOT NULL,
    report_name VARCHAR(20) NOT NULL,
    financial_year VARCHAR(20) NOT NULL,
    publish_date TIMESTAMP WITHOUT TIME ZONE,
    approved_date TIMESTAMP WITHOUT TIME ZONE,
    data_hash TEXT,
    CONSTRAINT stock_financials_data_hash_key UNIQUE (data_hash)
);

-- Stock Sector Wise Summary Table
CREATE TABLE stock_sector_wise_summary (
    id BIGSERIAL PRIMARY KEY,
    business_date DATE,
    sector_name VARCHAR(100),
    total_transaction NUMERIC(20,2),
    turn_over_values NUMERIC(20,2),
    turn_over_volume VARCHAR(50),
    created_at DATE,
    CONSTRAINT stock_sector_wise_summary_created_at_sector_name_key UNIQUE (created_at, sector_name)
);

-- Stock Symbol Sectors Table
CREATE TABLE stock_symbol_sectors (
    sector TEXT,
    symbol TEXT
);