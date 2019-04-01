import re
import datetime


def run_backtest():
    pass


def get_date(file_name):
    year, month, day = re.match(
        r'.*(\d\d\d\d)-(\d\d)-(\d\d).*', file_name).groups()
    return datetime.date(int(year), int(month), int(day))

