"""
    Created by Jhesed D. Tacadena on 11/11/17
    Automating querying of AirAsia flights
"""
import requests
import time
from bs4 import BeautifulSoup

class AirAsiaParser(object):

    url = 'https://booking.airasia.com/Flight/Select?o1={from_}&d1={to_}&culture=en-GB&dd1={depart_date}&ADT=1&s=true&mon=true&cc=PHP&c=false'
    info = "{ts_queried},{depart_date},{depart_time},{arrival_time},{from_},{to_},{price},{seats_left}"

    def __init__(self, from_, to_, depart_date):
        self.from_ = from_
        self.to_ = to_
        self.depart_date = depart_date  # i.e. YYYY-MM-DD


    def main(self):
        self.ts_queried = time.time()
        print(self.url.format(
            from_=self.from_, to_=self.to_, depart_date=self.depart_date))
        self.page = requests.get(self.url.format(
            from_=self.from_, to_=self.to_, depart_date=self.depart_date))
        self.soup = BeautifulSoup(self.page.content)
        self.get_price()
        self.get_seats_left()
        self.get_depart_arrive_time()
        self.get_info()

    def get_price(self):
        self.price = self.soup.find_all(class_='avail-fare-price')

    def get_seats_left(self):
        self.seats_left = self.soup.find_all('div', class_='avail-table-seats-remaining')

    def get_depart_arrive_time(self):
        details = self.soup.find_all('div', class_='avail-table-bold')
        self.depart_time = details[0]
        self.arrival_time = details[1]


    def get_info(self):
        info = self.info.format(
            ts_queried=self.ts_queried, depart_date=self.depart_date,
            depart_time=self.depart_time, arrival_time=self.arrival_time,
            from_=self.from_, to_=self.to_, price=self.price,
            seats_left=self.seats_left)
        print(info)


if __name__ == '__main__':
    ap = AirAsiaParser('MNL', 'MPH', '2017-11-14')
    ap.main()