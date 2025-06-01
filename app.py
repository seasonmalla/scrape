from flask import Flask, request, jsonify
from nepse import Nepse
from sqlalchemy import create_engine
import logging
import pandas as pd
from datetime import datetime, timedelta
import re
import os
from dotenv import load_dotenv
import httpx
from psycopg2 import sql, extras
import psycopg2.errors
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

import sys
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only use StreamHandler for Vercel compatibility
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
with app.app_context():
    """init rollbar module"""
    rollbar.init(
        '8e328fef1b784ce686ac78356f7ac2546b1b7a8b030c13bee02ee92d987a176aed173b018202c52c81ff9293c3a09ed1',
        # environment name - any string, like 'production' or 'development'
        'flasktest',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
    
nepse = Nepse()

dtype_spec = {
    'id': 'Int64',
    'businessDate': 'string',
    'securityId': 'Int64',
    'symbol': 'string',
    'securityName': 'string',
    'openPrice': 'float64',
    'highPrice': 'float64',
    'lowPrice': 'float64',
    'closePrice': 'float64',
    'totalTradedQuantity': 'float64',
    'totalTradedValue': 'float64',
    'previousDayClosePrice': 'float64',
    'fiftyTwoWeekHigh': 'float64',
    'fiftyTwoWeekLow': 'float64',
    'lastUpdatedTime': 'string',
    'lastUpdatedPrice': 'float64',
    'totalTrades': 'float64',
    'averageTradedPrice': 'float64',
    'marketCapitalization': 'float64'
}        

nepse.setTLSVerification(False)

@app.route('/')
def hello():
    print("DEBUG - in hello()")
    x = None
    x[5]
    return "Hello World!"

@app.route('/api/v1/market_status', methods=['GET'])
def market_status():
    logger.info('market_status endpoint accessed')
    try:
        # Get authorization headers
        logger.info('Getting authorization headers')
        response = nepse.getMarketStatus()        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error getting market status: {str(e)}")
        return jsonify({"message": "Failed to retrieve market status", "status": 500}), 500


@app.route('/api/v1/financial', methods=['POST'])
def financial():
    logger.info('financial endpoint accessed')
    data = request.get_json()
    
    try:
        # Validate request data
        validation = api_validation(data)
        if validation is not None:
            return jsonify(validation), validation['status']
        
        # Log the request
        logger.info("Received valid scrape request")
        # Check security code exists
        if 'security_id' not in data:
            logger.error("security_id is required")
            return jsonify({"message": "security_id is required", "status": 400}), 400
        if type(data['security_id']) is not int:
            logger.error("security_id must be an integer")
            return jsonify({"message": "security_id must be an integer", "status": 400}), 400
        
        security_id = get_security_id_from_price_volume(data['security_id'])
        if len(security_id) == 0:
            logger.error(f"Security ID {data['security_id']} not found")
            return jsonify({"message": f"Security ID {data['security_id']} not found", "status": 404}), 404
        else:
            try:
                # Get authorization headers
                logger.info('Getting authorization headers')
                auth_header = nepse.getAuthorizationHeaders()
                logger.info('Authorization successful')
                url=f'https://www.nepalstock.com.np/api/nots/application/reports/{data['security_id']}'
                client = httpx.Client(verify=False, http2=True, timeout=100)
                response = client.get(
                        url,
                        headers=(auth_header),
                    )
                if response.status_code == 200:
                    return jsonify({"status":"success","data":response.json()[0]}), 200
                else:
                    return jsonify({"message": "Failed to retrieve data", "status": response.status_code}), response.status_code
                # Get the authorization headers
            except Exception as e:
                logger.error(f"Error during login: {str(e)}")
                return jsonify({"message": "Login failed", "status": 500}), 500
        
    except Exception as e:
        logger.error(f"Error getting authorization headers: {str(e)}")
        return jsonify({"message": "Authorization failed", "status": 500}), 500
    
@app.route('/api/v1/divided', methods=['POST'])
def divided():
    logger.info('divided endpoint accessed')
    data = request.get_json()
    
    try:
        # Validate request data
        validation = api_validation(data)
        if validation is not None:
            return jsonify(validation), validation['status']
        
        # Log the request
        logger.info("Received valid scrape request")
        # Check security code exists
        if 'security_id' not in data:
            logger.error("security_id is required")
            return jsonify({"message": "security_id is required", "status": 400}), 400
        if type(data['security_id']) is not int:
            logger.error("security_id must be an integer")
            return jsonify({"message": "security_id must be an integer", "status": 400}), 400
        
        security_id = get_security_id_from_price_volume(data['security_id'])
        if len(security_id) == 0:
            logger.error(f"Security ID {data['security_id']} not found")
            return jsonify({"message": f"Security ID {data['security_id']} not found", "status": 404}), 404
        else:
            try:
                # Get authorization headers
                logger.info('Getting authorization headers')
                auth_header = nepse.getAuthorizationHeaders()
                logger.info('Authorization successful')
                url=f'https://www.nepalstock.com.np/api/nots/application/dividend/{data['security_id']}'
                client = httpx.Client(verify=False, http2=True, timeout=100)
                response = client.get(
                        url,
                        headers=(auth_header),
                    )
                if response.status_code == 200:
                    return jsonify({"status":"success","data":response.json()[0]}), 200
                else:
                    return jsonify({"message": "Failed to retrieve data", "status": response.status_code}), response.status_code
                # Get the authorization headers
            except Exception as e:
                logger.error(f"Error during login: {str(e)}")
                return jsonify({"message": "Login failed", "status": 500}), 500
        
    except Exception as e:
        logger.error(f"Error getting authorization headers: {str(e)}")
        return jsonify({"message": "Authorization failed", "status": 500}), 500
     

@app.route('/api/v1/scrape', methods=['POST'])
def save_price_volume_history():
    try:
        logger.info('Scrape endpoint start')
        # Get request data
        data = request.get_json()
        # Validate secret key
        validation = api_validation(data)
        if validation is not None:
            raise ValueError(validation['message'])
        # Log the request
        logger.info("Received valid scrape request")
        
        # Process the request
        result = retrieve_current_price_volume_history()
        
        # Return response
        return jsonify(result), 200
        
    except Exception as e:
        rollbar.report_exc_info()
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "message": "Exception occurred while processing the request",
            "status": 500,
            "error": str(e)
        }), 500
 
 
def api_validation(data):
    """
    Validate the request data for the API.
    """
    if not data:
        return {"message": "No data provided", "status": 400}
    
    secret_key = os.getenv('SECRET_KEY_SCRAPE')
    if not secret_key:
        return {"message": "Server configuration error", "status": 500}
    
    if 'secret_key_scrape' not in data:
        return {"message": "secret_key_scrape is required", "status": 400}
    
    if data['secret_key_scrape'] != secret_key:
        return {"message": "Invalid secret key", "status": 401}
    
    return None

def camel_to_snake(name):
    # Replace capital letters with underscore followed by lowercase letter
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def retrieve_current_price_volume_history():
    current_date = datetime.now() 
    current_weekday = current_date.weekday()
    
    if current_weekday in [4, 5]:  # 4 is Friday, 5 is Saturday
        logger.info(f"Current date {current_date.strftime('%Y-%m-%d')} is {'Friday' if current_weekday == 4 else 'Saturday'}")
        return {"message": "Market is closed on Friday and Saturday"}
    try:
        market_status = nepse.getMarketStatus()
        if market_status['isOpen'] != 'OPEN':
            logger.info(f"Market is currently {market_status['isOpen']}")
            return {"message": f"Market is currently {market_status['isOpen']}", "status": 200}
        current_date_str = current_date.strftime('%Y-%m-%d')
        data = nepse.getPriceVolumeHistory(current_date_str)
        return save_price_volume_history_df(data,current_date_str)
    except Exception as e:
        rollbar.report_exc_info()
        logger.error(f"Error retrieving current price volume history: {str(e)}")
        return {"message": "Exception occurred while retrieving current price volume history", "status": 500, "error": str(e)}

def save_price_volume_history_df(data,date):
    if len(data['content'])>0:
        df = pd.DataFrame(data['content'])
        df = df.astype(dtype_spec)
        df["businessDate"] = pd.to_datetime(df["businessDate"], errors="coerce")
        df['lastUpdatedTime'] = pd.to_datetime(
                df['lastUpdatedTime'],
                errors='coerce',
                format='%Y-%m-%dT%H:%M:%S.%f'
            )
        if 'id' in df.columns:
            df = df.drop(columns=['id'])
        df.columns = [camel_to_snake(col) for col in df.columns]
        if 'total_trades' in df.columns:
            df['total_trades'] = pd.to_numeric(df['total_trades'], errors='coerce')
        df = df.sort_values(by="business_date", ascending=True)
        df['business_date'] = df['business_date'].dt.strftime('%Y-%m-%d')
        response=insert_data(df)
        if response:
            logger.info(f"Data inserted successfully for {date}")
            return {"message": "success","status":200}
        else:
            logger.error(f"Error inserting data for {date}")
            return {"message": "error","status":500}
    else:
        logger.info(f"No data found for {date}")    
    
def insert_data(df):
    # Get database URL from environment variable
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable is not set")
        return False
        
    engine = create_engine(database_url)
    table_name = 'stock_prices'
    try:
        with engine.begin() as conn:
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
        return True
    except Exception as e:
        logger.error(f"Error inserting data into database:{e}")
        return False

def get_security_id_from_price_volume(securiry_id=None):
    # Get database URL from environment variable
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable is not set")
        return False
        
    engine = create_engine(database_url)
    table_name = 'stock_prices'
    try:
        with engine.begin() as conn:
            if securiry_id is not None:
            # If a specific security_id is provided, filter by it
                query = f"select distinct(security_id),symbol from {table_name} where security_id={securiry_id};"
            else:
                query = f"select distinct(security_id),symbol from {table_name} order by security_id;"
            df = pd.read_sql(query, conn)
        return df['security_id'].tolist()
    except Exception as e:
        logger.error(f"Error retrieving data from database:{e}")
        return False


if __name__ == '__main__':
    logger.info('Starting Flask application')
    app.run(debug=True,port=8000)
# 

