import pandas as pd
import numpy as np

headers = [
    'name',
    'country',
    'list',
    'sector',
    'industry',
    'ticker',
    'type',
    'report',
    '1d',
    '1w',
    '1m',
    '3m',
    '6m',
    '1y',
    '3y',
    'market-cap'
]


def trends(file_name):
    data = get_data(file_name)
    data = filter_swedish(data)
    data = filter_stocks(data)
    print('Sector overview')
    t1 = trends_per_interval(data, ['sector'], '1m')
    t2 = trends_per_interval(data, ['sector'], '3m')
    t3 = trends_per_interval(data, ['sector'], '6m')
    print('Industry details')
    td1 = trends_per_interval(data, ['sector', 'industry'], '1m')
    td2 = trends_per_interval(data, ['sector', 'industry'], '3m')
    td3 = trends_per_interval(data, ['sector', 'industry'], '6m')
    print('Sectors trending over all intervals')
    print('-----------------------------------')
    for sector in sorted(t1 | t2 | t3):
        print(sector)
    print()
    print()
    print('Industries trending over all intervals')
    print('--------------------------------------')
    for industry in sorted(td1 & td2 & td3):
        print('  -  '.join(industry))


def trends_per_interval(data, grouping, span):
    data = data.drop(data[data[span].isnull()].index)
    aggregated = data.groupby(grouping)[span].aggregate(['mean', np.median, 'std', 'count'])
    aggregated = aggregated.sort_values('median', ascending=False)
    aggregated = aggregated.head(10)
    output = aggregated.to_string(formatters={
        'mean': '{:.0%}'.format,
        'median': '{:.0%}'.format,
        'std': '{:.0%}'.format
    })
    print(span)
    print('-'*len(span))
    print(output)
    print()
    print()
    return set(aggregated.index.values)


def filter_swedish(data):
    return data[data['country'].isin(['Sverige'])]


def filter_stocks(data):
    return data[data['type'].isin(['Aktier'])]


def get_data(file_name):
    data = pd.read_excel(file_name)
    data = data[1:]
    data.columns = headers
    text_columns = ['name', 'country', 'list', 'sector', 'industry', 'type', 'report', 'ticker']
    numeric_columns = list(set(headers) - set(text_columns))
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric)
    return data
