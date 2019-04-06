import re
import datetime
import os


def run_backtest():
    folder = __file__.replace('backtest.py', '')
    run_backtest_in_folder(folder + '/data/')


def run_backtest_in_folder(data_dir):
    for f in os.listdir(data_dir):
        if f[-5:] == '.xlsx':
            date = get_date_from_file_name(f)
            if date:
                print(f, date)


def get_date_from_file_name(file_name):
    try:
        year, month, day = re.match(
            r'.*(\d\d\d\d)-(\d\d)-(\d\d).*', file_name).groups()
        return datetime.date(int(year), int(month), int(day))
    except AttributeError:
        return None

