import backtest as bt
import click


@click.command()
@click.option('--file-name')
@click.option('--backtest', flag_value=True, default=False)
@click.option('--runimport', flag_value=True, default=False)
@click.option('--algo', default=None)
def run(file_name, backtest, runimport, algo):
    if not any([file_name, backtest, runimport]):
        print('Need to some arguments')
        return

    if algo:
        screener_algo = __import__(algo.replace('.py', ''))
    else:
        import screener as screener_algo

    if not backtest and file_name:
        picks = screener_algo.screen(file_name)
        print(picks)
    if backtest and file_name:
        bt.run_backtest_on_file(file_name, screener_algo.screen)


if __name__ == '__main__':
    run()

