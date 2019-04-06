import screener
import backtest as bt
import click


@click.command()
@click.option('--file-name')
@click.option('--backtest', flag_value=True, default=False)
@click.option('--runimport', flag_value=True, default=False)
def run(file_name, backtest, runimport):
    if not any([file_name, backtest, runimport]):
        print('Need to some arguments')
        return
    if not backtest and file_name:
        picks = screener.screen(file_name)
        print(picks)
    if backtest and file_name:
        bt.run_backtest_on_file(file_name)


if __name__ == '__main__':
    run()

