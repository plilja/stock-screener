import backtest as bt
import click
from borsdata_api import BorsdataApi
import sector_trends as trends


@click.command()
@click.option('--file-name')
@click.option('--sector-trends', flag_value=True, default=False)
@click.option('--backtest', flag_value=True, default=False)
@click.option('--runimport', flag_value=True, default=False)
@click.option('--algo', default=None)
def run(file_name, sector_trends, backtest, runimport, algo):
    if not any([file_name, backtest, runimport]):
        print('Need to some arguments')
        return

    if algo:
        screener_algo = __import__(algo.replace('.py', ''))
    else:
        import screener as screener_algo

    if sector_trends:
        trends.trends(file_name)
    elif not backtest and file_name:
        picks = screener_algo.screen(file_name, True, True)
        borsdata = BorsdataApi()
        for pick in picks:
            instrument = borsdata.get_instrument_by_yahoo(pick)
            if instrument:
                print(instrument.name)
            else:
                print(pick)
    elif backtest and file_name:
        bt.run_backtest_on_file(file_name, screener_algo.screen)


if __name__ == '__main__':
    run()
