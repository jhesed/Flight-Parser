"""
    Created by Jhesed D. Tacadena on 11/11/17
    Automating querying of AirAsia flights
"""

import requests
import time
from bs4 import BeautifulSoup
from base import BaseParser

class CebuPacific(BaseParser):

    url = 'https://beta.cebupacificair.com/Flight/Select?o1={from_}&d1={to_}&o2=&d2=&dd1={depart_date}&ADT=1&CHD=0&INF=0&inl=0&pos=cebu.ph&culture='
    header = 'TS Queried, Depart Date, Depart Time, Arrival Time, From, To, Lowest Price, Seats Left\n'
    info = "{ts_queried},{depart_date},{depart_time},{arrival_time},{from_},{to_},{price},{seats_left}\n"
    report_file = 'reports/cebupacific.{}.csv'


    def main(self):
        self.ts_queried = time.time()
        print(self.url.format(
            from_=self.from_, to_=self.to_, depart_date=self.depart_date))
        self.page = requests.get(self.url.format(
            from_=self.from_, to_=self.to_, depart_date=self.depart_date))
        self.soup = BeautifulSoup(self.page.content)
        self.get_price()
        self.get_seats_left()
        self.get_info()

    def get_price(self):
        prices = self.soup.find_all('label', class_='fare-amount')
        lowest_price = 9999999999999999
        for price in prices:
            float_price = float(price['data-amount'])
            if float_price < lowest_price:
                lowest_price = float_price
                self.get_depart_arrive_time(price.parent.find('input')['value'])

        self.price = lowest_price

    def get_seats_left(self):
        self.seats_left = 'NA'

    def get_depart_arrive_time(self, depart_arrival_value):
        depart_start_index =  depart_arrival_value.index(self.from_)
        arrival_start_index = depart_arrival_value.index(self.to_)
        self.depart_time = depart_arrival_value[depart_start_index:arrival_start_index].replace('~', ' ').replace(self.from_, '')
        self.arrival_time = depart_arrival_value[arrival_start_index:].replace('~', ' ').replace(self.to_, '')



if __name__ == '__main__':
    ap = CebuPacific('MNL', 'MPH', '2017-11')
    ap.main()