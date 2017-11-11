"""
    Created by Jhesed D. Tacadena on 11/12/17
"""

import time

class BaseParser(object):

    url = ''
    header = ''
    info = '\n'
    report_file = 'reports/s'

    def __init__(self, from_, to_, depart_date):
        self.from_ = from_
        self.to_ = to_
        self.depart_date = depart_date  # i.e. YYYY-MM-DD
        self.file_name = self.report_file.format(time.time())

        # CSV header
        self.save_to_csv(self.file_name, self.header)

        # default values
        self.ts_queried = None
        self.depart_time = None
        self.arrival_time = None
        self.price = None
        self.seats_left = None

    def get_info(self):
        info = self.info.format(
            ts_queried=self.ts_queried, depart_date=self.depart_date,
            depart_time=self.depart_time, arrival_time=self.arrival_time,
            from_=self.from_, to_=self.to_, price=self.price,
            seats_left=self.seats_left)

        self.save_to_csv(self.file_name, info)

    def save_to_csv(self, file_name, data):
        with open(file_name, 'a') as report_file:
            report_file.write(data)
