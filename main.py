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
    if file_name:
        picks = screener.screen(file_name, True)
        print(picks)
    if backtest:
        bt.run_backtest()


if __name__ == '__main__':
    run()

