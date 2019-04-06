import pandas as pd

headers = [
    'namn',
    'land',
    'ev',
    'peg',
    'branch',
    'f-score',
    'rörelsemarginal 5',
    'vinsttillväxt',
    'vinsttillväxt 5',
    'ek-tillväxt',
    'ek-tillväxt 5',
    'omsättningstillväxt',
    'omsättningstillväxt 5',
    'direktavkastning',
    'kurs',
    'roa',
    'pe 10-årslägsta',
    'bruttomarginal',
    'bruttomarginal 5',
    'pe',
    'ps',
    'ev/ebit',
    'pb',
    'rörelsemarginal',
    'p/pcf',
    'roe',
    'roe 5',
    'yahoo-ticker',
    'op-kassaflöde',
    'op-kassaflöde 5',
    'antal-aktier 5'
]


def screen(file_name, write_output=True, nordic_only=False):
    data = get_data(file_name)
    data['sum'] = 0
    if nordic_only:
        data = pick_nordic_only(data)
    pick_quality(data)
    pick_cheap(data)
    pick_quality_relative_mean(data)
    pick_cheap_relative_mean(data)
    data = data.sort_values('sum', ascending=False)
    if write_output:
        data.head(100).to_excel('output.xlsx')
    return data.head(10)['yahoo-ticker'].tolist()


def pick_nordic_only(data):
    return data[data['land'].isin(['Sverige', 'Norge', 'Finland', 'Danmark'])]


def pick_cheap_relative_mean(data):
    data = data.drop(data[data.pe.isnull()].index)
    country_pe = data[data['pe'] >= 6].groupby(['land'])
    sector_pe = data[data['pe'] >= 6].groupby(['land', 'branch'])
    sector_ps = data.groupby(['land', 'branch'], as_index=True)
    # PE is positive and in the 25% lowest quantile in the country
    d1 = data.apply(axis=1, func=lambda x: x['pe'] >= 6 and x['pe'] < country_pe.get_group(
        x['land'])['pe'].quantile(0.25))
    data['rc1'] = d1.astype(int)
    # PE is positive and lower than average PE of companies in same sector
    d2 = data.apply(axis=1, func=lambda x: x['pe'] >= 6 and x['pe'] < sector_pe.get_group(
        (x['land'], x['branch']))['pe'].mean())
    data['rc2'] = d2.astype(int)
    # PS is lower than average of companies in same sector
    d3 = data.apply(axis=1, func=lambda x: x['ps'] < sector_ps.get_group(
        (x['land'], x['branch']))['ps'].mean())
    data['rc3'] = d3.astype(int)
    data['sum'] = data['sum'] + data['rc1'] + data['rc2'] + data['rc3']
    return data


def pick_quality_relative_mean(data):
    country_roa = data.groupby(['land'])
    sector_roa = data.groupby(['land', 'branch'])
    sector_earnings_growth = data.groupby(['land', 'branch'])
    sector_sales_growth = data.groupby(['land', 'branch'])

    # ROA is better than average ROA of country
    d1 = data.apply(axis=1, func=lambda x: x['roa'] >= 0 and x['roa'] > country_roa.get_group(
        x['land'])['roa'].mean())
    data['rq1'] = d1.astype(int)
    # ROA is better than average ROA of sector
    d2 = data.apply(axis=1, func=lambda x: x['roa'] >= 0 and x['roa'] > sector_roa.get_group(
        (x['land'], x['branch']))['roa'].mean())
    data['rq2'] = d2.astype(int)
    # Earnings growth is in top 25 % of sector
    d3 = data.apply(axis=1, func=lambda x: x['vinsttillväxt'] >= 0 and x['vinsttillväxt'] > sector_earnings_growth.get_group(
        (x['land'], x['branch']))['vinsttillväxt'].quantile(0.75))
    data['rq3'] = d3.astype(int)
    # Sales growth is in top 25 % of sector
    d4 = data.apply(axis=1, func=lambda x: x['omsättningstillväxt'] >= 0 and x['omsättningstillväxt'] > sector_sales_growth.get_group(
        (x['land'], x['branch']))['omsättningstillväxt'].quantile(0.75))
    data['rq4'] = d4.astype(int)
    data['sum'] = data['sum'] + data['rq1'] + \
        data['rq2'] + data['rq3'] + data['rq4']


def pick_cheap(data):
    data['c1'] = 0.25 * (data['pe'] < 25).astype(int)
    data['c2'] = 0.5 * (data['pe'] < 18).astype(int)
    data['c3'] = 1 * (data['pe'] < 15).astype(int)
    data['c4'] = 1.25 * (data['pe'] < 13).astype(int)
    data['c5'] = (data['ps'] < 3).astype(int)
    data['c6'] = (data['pb'] < 2).astype(int)
    data['c7'] = (data['peg'] < 1).astype(int)
    data['c8'] = (data['peg'] >= 0).astype(int)
    data['c9'] = (data['p/pcf'] >= 0).astype(int)
    data['c10'] = (data['p/pcf'] < 20).astype(int)
    data['sum'] = data['sum'] + data['c1'] + data['c2'] + data['c3'] + data['c4'] + \
        data['c5'] + data['c6'] + data['c7'] + \
        data['c8'] + data['c9'] + data['c10']


def pick_quality(data):
    data['q1'] = (data['roe'] > 0.12).astype(int)
    data['q2'] = 2 * (data['roa'] > 0.08).astype(int)
    data['q3'] = (data['rörelsemarginal 5'] <
                  data['rörelsemarginal']).astype(int)
    data['q4'] = (data['bruttomarginal 5'] <
                  data['bruttomarginal']).astype(int)
    data['q5'] = 2 * (data['op-kassaflöde'] >= 0).astype(int)
    data['q6'] = (data['op-kassaflöde 5'] >= 0).astype(int)
    data['q7'] = (data['vinsttillväxt 5'] >= 0.1).astype(int)
    data['q8'] = (data['vinsttillväxt'] >= 0.0).astype(int)
    data['q9'] = (data['omsättningstillväxt 5'] >= 0.1).astype(int)
    data['q10'] = (data['omsättningstillväxt'] >= 0.0).astype(int)
    data['q11'] = 4 * (data['pe 10-årslägsta'] >= 0).astype(int)
    data['q12'] = (data['direktavkastning'] > 0).astype(int)
    data['q13'] = (data['antal-aktier 5'] < 0.06).astype(int)
    data['q14'] = (data['roe 5'] < data['roe']).astype(int)
    data['q15'] = 2 * (data['f-score'] >= 7).astype(int)
    data['q16'] = (data['ek-tillväxt'] >= 0).astype(int)
    data['q17'] = (data['ek-tillväxt 5'] >= 0).astype(int)
    data['q18'] = 1 * (data['pe'] >= 0).astype(int)
    data['q19'] = 1 * (data['pe'] >= 7).astype(int)
    data['sum'] = data['sum'] + data['q1'] + data['q2'] + data['q3'] + data['q4'] + \
        data['q5'] + data['q6'] + data['q7'] + data['q8'] + data['q9'] + \
        data['q10'] + data['q11'] + data['q12'] + data['q13'] + data['q14'] + \
        data['q15'] + data['q16'] + data['q17'] + data['q18'] + data['q19']


def get_data(file_name):
    data = pd.read_excel(file_name)
    data = data[1:]
    data.columns = headers
    text_columns = ['namn', 'land', 'branch', 'yahoo-ticker']
    numeric_columns = list(set(headers) - set(text_columns))
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric)
    return data

