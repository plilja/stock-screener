import re
import datetime
import os
import logging
import screener
from borsdata_api import BorsdataApi


def run_backtest():
    folder = __file__.replace('backtest.py', '')
    run_backtest_in_folder(folder + '/data/')


def run_backtest_in_folder(data_dir):
    for f in os.listdir(data_dir):
        if f[-5:] == '.xlsx':
            run_backtest_on_file(f)


def run_backtest_on_file(file_name):
    date = get_date_from_file_name(file_name)
    today = datetime.date.today()
    if not date:
        logging.warning("Can't run backtest on file with name %s, skipping" % file_name)
        return
    picks = screener.screen(file_name, False, True)
    borsdata = BorsdataApi()
    acc = 0
    count = 0
    for yahoo_ticker in picks:
        instrument = borsdata.get_instrument_by_yahoo(yahoo_ticker)
        if not instrument:
            logging.warning("""Instrument with yahoo ticker %s could
                    not be found, skipping. Note that this
                    might overestimate the result if the company
                    went bankrupt. Please investigate the ticker
                    as this might indicate that the screener has
                    made a really poor pick.""" % yahoo_ticker)
            continue
        price1 = instrument.get_price(date)
        price2 = instrument.get_price(today)
        if price1 == 0 or None in [price1, price2]:
            logging.warning('Instrument %s is lacking price or has zero price, skipping' % instrument.name)
            continue
        change = 100 * (price2 / price1 - 1)
        print('Percentage change on %s was %.2f%%' % (instrument.name, change))
        acc += change
        count += 1
    percentage_change = acc / count
    days = (today - date).days
    print('Total percentage change was %.1f%% over a period of %d days' % (percentage_change, days))


def get_date_from_file_name(file_name):
    try:
        year, month, day = re.match(
            r'.*(\d\d\d\d)-(\d\d)-(\d\d).*', file_name).groups()
        return datetime.date(int(year), int(month), int(day))
    except AttributeError:
        return None

