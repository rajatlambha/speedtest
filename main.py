import requests
import json
from bs4 import BeautifulSoup
import csv 
import pymssql
import mysql.connector
import mysql.connector
from mysql.connector import Error
import os



class SpeedTest():
    def __init__(self):
        self.url = "https://www.speedtest.net/global-index"
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        

        
    

    def mobile_data(self):
        data = self.soup.find("div", {"id": "column-mobileMedian"}).find("div",
                                                            {"class": "specific-results"}).find("table", {"list-results"}).find("tbody")
        rows = data.find_all("tr")
        
        mobile_data = self.get_table_data(rows)
        self.create_csv(mobile_data,"mobile-speedtest.csv")
        values = []
        for row in mobile_data:
            values.append((row[0],row[1],row[2]))
        # self.insert_data(values,"mobiledata")

        
    def fixed_data(self):
        data = self.soup.find("div", {"id": "column-fixedMedian"}).find("div",
                                                            {"class": "specific-results"}).find("table", {"list-results"}).find("tbody")
        rows = data.find_all("tr")
        fixedData = self.get_table_data(rows)
        self.create_csv(fixedData,"fixed-speedtest.csv")
        values = []
        for row in fixedData:
            values.append((row[0],row[1],row[2]))
        self.insert_data(values,"fixeddata")
            
        # self.db.insert_data(values,"fixed_speedtest")
        
        
    def get_table_data(self,rows):
        final_data = []
        count = 1
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            if len(cols)>1:
                row_table = [count,cols[2],cols[3]]
                count = count + 1
                final_data.append(row_table)
        return final_data
    
    def create_csv(self,final_data,file_name):
        headers = ["Country", "Speed"]
        fileName = file_name

        with open(fileName, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(headers)
            writer.writerows(final_data)

        csvFile.close()
    
    def insert_data(self,values,table):
        try:
            connection = mysql.connector.connect(host=os.environ.get('host'),
                                                database=os.environ.get('database'),
                                                user=os.environ.get('user'),
                                                password = os.environ.get('password'))
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                values = tuple(values)
                final_value = ','.join([str(item) for item in (values)])
                query = f"""INSERT INTO {table}  VALUES {final_value}"""
                cursor.execute(query)
                connection.commit()
                
                print(f'Record inserted successfully into {table} table')

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
        
if __name__ == "__main__":
    speed = SpeedTest()
    speed.mobile_data()
    speed.fixed_data()