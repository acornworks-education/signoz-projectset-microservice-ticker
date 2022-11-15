import psycopg2
import os
import logging

logging.basicConfig(level=logging.DEBUG)

DB_INFO = {
    'database': 'postgres' if not 'TICKER_DATABASE' in os.environ else os.environ['TICKER_DATABASE'],
    'host': 'localhost' if not 'TICKER_HOST' in os.environ else os.environ['TICKER_HOST'],
    'user': 'postgres' if not 'TICKER_USER' in os.environ else os.environ['TICKER_USER'],
    'password': 'P@ssw0rd' if not 'TICKER_PASSWORD' in os.environ else os.environ['TICKER_PASSWORD'],
    'port': '65432' if not 'TICKER_PORT' in os.environ else os.environ['TICKER_PORT']
}

def get_tickers():
    with psycopg2.connect(**DB_INFO) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT TICKER, NAME FROM TRADE.TICKER')
            result_list = cursor.fetchall()

    return list(map(lambda x: {'ticker': x[0], 'name': x[1]}, result_list))

def add_ticker(ticker_info):
    if (not 'ticker' in ticker_info) or (ticker_info['ticker'] is None) or (len(ticker_info['ticker']) == 0):
        raise BaseException('KEY_TICKER_NAME_SHOULD_BE_DEFINED')
    
    if (not 'name' in ticker_info) or ticker_info['name'] is None:
        ticker_info['name'] = ''
    
    sql_query = 'INSERT INTO TRADE.TICKER(TICKER, NAME) VALUES(''%(ticker)s'', ''%(name)s'') ON CONFLICT(TICKER) DO UPDATE SET TICKER=EXCLUDED.TICKER'

    with psycopg2.connect(**DB_INFO) as conn:
        with conn.cursor() as cursor:
            logging.info('Try to save a ticker for %s' % ticker_info['ticker'])

            cursor.execute(sql_query, (ticker_info))
            logging.info('Succeed to save the ticker for %s' % ticker_info['ticker'])

            cursor.execute('SELECT TICKER, NAME FROM TRADE.TICKER WHERE TICKER=%(ticker)s', ticker_info)
            ticker_info = cursor.fetchone()

    return {'ticker': ticker_info[0], 'name': ticker_info[1]}

def remove_ticker(ticker_info):
    if (not 'ticker' in ticker_info) or (ticker_info['ticker'] is None) or (len(ticker_info['ticker']) == 0):
        raise BaseException('KEY_TICKER_SHOULD_BE_DEFINED')
    
    sql_query = 'DELETE FROM TRADE.TICKER WHERE TICKER=%(ticker)s'
    
    with psycopg2.connect(**DB_INFO) as conn:
        with conn.cursor() as cursor:
            logging.info('Try to delete a ticker for %s' % ticker_info['ticker'])

            cursor.execute(sql_query, (ticker_info))
            logging.info('Succeed to delete the ticker for %s' % ticker_info['ticker'])
    
    ticker_info['name'] = ''

    return ticker_info


        