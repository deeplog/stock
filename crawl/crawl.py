import duckdb
from datetime import datetime, timedelta
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import FinanceDataReader as fdr
import pandas as pd
import yfinance as yf

def get_stock(code, start_date, end_date, market):
    def try_download(func, *args, **kwargs):
        try:
            data = func(*args, **kwargs)
            if not data.empty:
                return data
        except Exception as e:
            pass
        return pd.DataFrame()

    market = market.lower()

    if market in ['kospi', 'kosdaq']:
        # 한국 주식 다운로드
        df = try_download(fdr.DataReader, code, start_date, end_date)
        if not df.empty:
            return df

        # Yahoo Finance로 시도 (KOSPI)
        df = try_download(yf.download, f"{code}.KS", start=start_date, end=end_date, progress=False)
        if not df.empty:
            return df

        # Yahoo Finance로 시도 (KOSDAQ)
        df = try_download(yf.download, f"{code}.KQ", start=start_date, end=end_date, progress=False)
        if not df.empty:
            return df

    elif market == 'nasdaq':
        # NASDAQ 주식 다운로드
        df = try_download(yf.download, code, start=start_date, end=end_date, progress=False)
        if not df.empty:
            return df

    return pd.DataFrame()
def download_stocks(start_date, end_date, market):
    stocks=get_stock_list(market)
    for index, row in tqdm(stocks.iterrows(), total=len(stocks), desc=f"{market} 업데이트 중"):
        code = row['Code']
        name = row['Name']
        download_stock(code, name, start_date, end_date, market)

def download_stock(code, name, start_date, end_date, market):
        df = get_stock(code, start_date, end_date, market)
        if not df.empty:
            file_path = f'../db/{market.lower()}/{name}.parquet'
            df.to_parquet(file_path)
def get_stock_list(market):
    stocks = fdr.StockListing(market)
    if market in ['KOSPI','KOSDAQ']:
        stocks = stocks[['Code','Name']]
    elif market in ['NASDAQ']:
        stocks = stocks[['Symbol','Symbol']]
        stocks.columns=['Code','Name']
    else:
        return pd.DataFrame()
    return stocks
def optimize_dtypes(df):
    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col] = df[col].astype('float32')
        elif df[col].dtype == 'int64':
            df[col] = df[col].astype('int32')
    return df

def update_stock(ticker, name, market):
    try:
        file_path = f'../db/{market.lower()}/{name}.parquet'

        con = duckdb.connect(database=':memory:')

        if os.path.exists(file_path):
            last_row = con.execute(f"SELECT * FROM parquet_scan('{file_path}') ORDER BY date DESC LIMIT 1").fetchdf()
            if not last_row.empty:
                last_date = last_row['Date'][0]
                start_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                start_date = "2018-01-01"
        else:
            start_date = "2018-01-01"

        end_date = datetime.now().strftime("%Y-%m-%d")

        if start_date < end_date:
            new_data = get_stock(ticker, start_date, end_date, market)
            if new_data is not None and not new_data.empty:
                new_data = optimize_dtypes(new_data)
                if os.path.exists(file_path):
                    old_data = con.execute(f"SELECT * FROM parquet_scan('{file_path}')").fetchdf().set_index('Date')
                    update_data = pd.concat([new_data, old_data], axis=0).drop_duplicates()
                    update_data.to_parquet(file_path, index=True)
                else:
                    new_data.to_parquet(file_path, index=True)

        con.close()
        return True
    except Exception as e:
        return False

def update_stocks_parallel(tickers, market, chunk_size=50, max_workers=10):
    total_tickers = len(tickers)
    updated_count = 0
    failed_count = 0

    #dataframe을 dict로 변경
    stocks_list = tickers.to_dict('records')
    tickers = [{'Code': stock['Code'], 'Name': stock['Name']} for stock in stocks_list]

    with tqdm(total=total_tickers, desc="Total progress", position=0) as total_pbar:
        for i in range(0, total_tickers, chunk_size):
            chunk = tickers[i:i+chunk_size]
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(update_stock, stock['Code'], stock['Name'], market): stock['Code'] for stock in chunk}
                for future in as_completed(futures):
                    ticker = futures[future]
                    if future.result():
                        updated_count += 1
                    else:
                        failed_count += 1
                    total_pbar.update(1)

    print(f"\nUpdate completed. Successfully updated: {updated_count}, Failed: {failed_count}")

def get_market(market):
    market = market.upper()
    tickers = get_stock_list(market)
    print(f"Starting update for {len(tickers)} stocks")
    update_stocks_parallel(tickers, market)
    print("All updates completed")

if __name__=="__main__":
    for market in ['kospi','kosdaq','nasdaq']:
        get_market(market)