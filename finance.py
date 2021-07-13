from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other, get_quote_table

""" pull historical data for Netflix (NFLX) """
nflx = get_data("NFLX")

print(nflx)