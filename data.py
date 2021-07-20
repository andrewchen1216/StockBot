import requests
import sqlite3
import time
import yfinance as yf
from bs4 import BeautifulSoup


class StockBot:
    URL = "http://openinsider.com/latest-insider-trading"
    
    def __init__(self):
        self.con = sqlite3.connect("/Users/andrew/Documents/Personal Project/StockBot/stock.db")
        self.cur = self.con.cursor()
    
    #Two tables
    """
        1 table where we hold 50-10+
            To_the_moon(ticker, purchase price, date)
        1 table where we buy and sell 50-10 
            Index_fund(ticker,been_purchased)
                ticker_idtable(purchase, selling, date_purchase,date_sell,profit)
                
        1 table where we buy and sell 10 and lower stocks 
            Penny_stocks(ticker,been_purchased)
                table(purchase, selling, date_purchase,date_sell,profit)

        All stocks will be based on insider trading news 
    """
    def create_database(self):
        self.con = sqlite3.connect("/Users/andrew/Documents/Personal Project/StockBot/stock.db")
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE To_the_moon
               (ticker,purchase_price,date)''')
        self.con.commit()


    def insert_data(self, datalist):
        #datalist = [ticker,price,date]
        self.cur.execute("INSERT INTO To_the_moon VALUES {ticker},{price},{date})".format(ticker = datalist[0],price = datalist[1],date= datalist[2]))
        self.con.commit()
        
    
    def retrieve_data(self):
        for row in self.cur.execute('SELECT * FROM To_the_moon ORDER BY purchase_price'):
            print(row)
        
    def find_all_tables(self):
        res = self.con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res.fetchall():
            print(name[0])

    def close_database(self):
        self.con.close()
    

    #Grab ticker information for each stock 
    def get_ticker_price(self, ticker):
        stock = yf.Ticker(ticker)
        return stock.info['currentPrice']
        

    #Grabs data from the last hour 
    def get_data_hour(self):
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
        table = soup.find("table",attrs={"class":"tinytable"})
        data = table.find("tbody")
        dataset = []
        for row in data.find_all("tr"):
            curr_row = []
            #Adds all of the data from a single row into a list 
            for col in row.find_all("td")[1:10]:
                curr_row.append(col.get_text())
            #Checking the time period, with the filing date to be within the
            #last hour 
            curr_hour = time.localtime().tm_hour
            time_filed = curr_row[0];
            filed_hour = time_filed[11:13]
            #breaks loop if the time filed is not within the range,
            #prevents constantly checking the same invalid times
            if((int(filed_hour) >= curr_hour - 1) and (int(filed_hour) < curr_hour)):
                dataset.append(curr_row)
            else:
                break
        return dataset




    #Grabs data from the whole website 
    def get_data(self):
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
        table = soup.find("table",attrs={"class":"tinytable"})
        data = table.find("tbody")
        dataset = []
        for row in data.find_all("tr"):
            curr_row = []
            for col in row.find_all("td")[1:10]:
                print(type(col.get_text()))
                curr_row.append(col.get_text())
            dataset.append(curr_row)
        print(dataset)


if __name__ == '__main__':
    bot = StockBot()
    
    bot.find_all_tables()
    bot.close_database()
    # general while loop will be in here 

