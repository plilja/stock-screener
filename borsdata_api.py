import requests
import json
import datetime
import logging
import time

_country_map = {}
_country_map[1] = 'SE'
_country_map[2] = 'NO'
_country_map[3] = 'FI'
_country_map[4] = 'DK'

with open('borsdata_protected/api_key.txt') as f:
    _api_key = f.readline().strip()


def _avoid_rate_limit():
    time.sleep(0.51)


class Instrument:
    def __init__(self, params):
        self.id = params['insId']
        self.name = params['name']
        self.yahoo = params['yahoo']
        self.isin = params['isin']
        self.country = _country_map[params['countryId']]

    def get_price(self, day):
        _avoid_rate_limit()
        fr = day
        to = day + datetime.timedelta(days=4)  # Overfetch in case requested date is a weekend
        r = requests.get('https://apiservice.borsdata.se/v1/instruments/%d/stockprices?authKey=%s&from=%s&to=%s' % (self.id, _api_key, fr, to))
        if r.status_code != 200:
            logging.warning('Got unexpected status code when calling Borsdata %d' % r.status_code)
            return None
        else:
            body = r.json()
            prices = body['stockPricesList']
            if prices:
                return prices[0]['c']
            else:
                return None


class BorsdataApi:
    def __init__(self):
        self.instruments = {}
        self.yahoo_ticker_to_id = {}
        with open('borsdata_protected/instruments.json') as ins:
            instruments = json.load(ins)
            for i in instruments['instruments']:
                instrument = Instrument(i)
                self.instruments[instrument.id] = instrument
                self.yahoo_ticker_to_id[instrument.yahoo] = instrument.id

    def get_instrument_by_id(self, id):
        return self.instruments[id]

    def get_instrument_by_yahoo_ticker(self, yahoo_ticker):
        return self.get_instrument_by_id(self.yahoo_ticker_to_id[yahoo_ticker])


if __name__ == '__main__':
    b = BorsdataApi()
    assert(b.get_instrument_by_yahoo_ticker('ABB.ST').id == 3)
    assert(b.get_instrument_by_yahoo_ticker('ABB.ST').name == 'ABB')
    assert(b.get_instrument_by_yahoo_ticker('ABB.ST').country == 'SE')
    assert(b.get_instrument_by_yahoo_ticker('ABB.ST').isin == 'CH0012221716')
    weekend_day = datetime.date(2017, 10, 1)
    business_day = datetime.date(2017, 10, 2)
    assert(b.get_instrument_by_yahoo_ticker('ABB.ST').get_price(weekend_day) == 202.9)
    assert(b.get_instrument_by_yahoo_ticker('ABB.ST').get_price(business_day) == 202.9)
    assert(b.get_instrument_by_yahoo_ticker('ORK.OL').id == 944)
    assert(b.get_instrument_by_yahoo_ticker('ORK.OL').name == 'Orkla')
    assert(b.get_instrument_by_yahoo_ticker('ORK.OL').country == 'NO')
    assert(b.get_instrument_by_yahoo_ticker('ORK.OL').isin == 'NO0003733800')
    assert(b.get_instrument_by_yahoo_ticker('ORK.OL').get_price(weekend_day) == 82.25)
    assert(b.get_instrument_by_yahoo_ticker('ORK.OL').get_price(business_day) == 82.25)

