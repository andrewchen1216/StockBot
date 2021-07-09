import requests
import sqlite3
import time
from bs4 import BeautifulSoup

class StockBot:
    URL = "http://openinsider.com/latest-insider-trading"
    
    def __init__(self):
        pass
    
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
            if((int(filed_hour) >= curr_hour - 3) and (int(filed_hour) < curr_hour)):
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
    bot.get_data_hour()

