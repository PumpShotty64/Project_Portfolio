# abbreviates import names
import project3_download_info as pdi
import project3_indicators as pi
import project3_signal_strategies as pss


'''
Gathers user input
Outputs a tuple of commands
'''
def _user_input() -> tuple:

    # gather input
    symbolInput = input().strip()
    dayInput = int(input().strip())
    strategyInput = input().strip()

    return symbolInput, dayInput, strategyInput


'''creates an indicator depending on command'''
def _create_indicator(strat_input: str) -> 'indicatorObject':

    # creates object class depending on action
    if strat_input[:2] == 'TR':
        indicatorObject = pi.TrueRange()
    elif strat_input[:2] == 'MP':
        indicatorObject = pi.SimpleMovingAveragePrice()
    elif strat_input[:2] == 'MV':
        indicatorObject = pi.SimpleMovingAverageVolume()
    elif strat_input[:2] == 'DP':
        indicatorObject = pi.DirectionalIndicatorPrice()
    elif strat_input[:2] == 'DV':
        indicatorObject = pi.DirectionalIndicatorVolume()

    return indicatorObject



'''stores the information needed for the indicator and generates an indicator output'''
def _store_indicator_info(chartsDict: dict, index: int, indicator_object, user_input: tuple) -> tuple:

    # stores information in object
    indicatorStoredData = indicator_object.store_data(chartsDict, index, user_input)

    # generates indicator value
    indicatorVal = indicator_object.generate()

    return indicatorVal, indicatorStoredData


'''creates an signal strategy depending on command'''
def _create_signal_strategy(strat_input: str) -> 'sigstratObject':

    # creates object depending on what signal strategy chosen
    if strat_input[:2] == 'TR':
        sigstratObject = pss.TRCalc()
    elif strat_input[:2] == 'MP':
        sigstratObject = pss.MPCalc()
    elif strat_input[:2] == 'MV':
        sigstratObject = pss.MVCalc()
    elif strat_input[:2] == 'DP':
        sigstratObject = pss.DPCalc()
    elif strat_input[:2] == 'DV':
        sigstratObject = pss.DVCalc()

    return sigstratObject


'''generates a string output '''
def _store_signal_strategy(indi_object_data_list: list, indiValList: list, sigstrat_object, index: int) -> str:

    # generates signal strategy
    buy_or_sell = sigstrat_object.calculate(indi_object_data_list, indiValList, index)

    return buy_or_sell


'''prints out all the information'''
def _print_stock_info(stock_dict: dict, indicator_list: list, buy_sell:list, symbol_input: str) -> None:

    # accesses company information
    stock_stats = stock_dict[symbol_input.upper()]['stats']
    stock_chart = stock_dict[symbol_input.upper()]['chart']
    index = 0

    # prints company information
    print(stock_stats['symbol'])
    print(stock_stats['companyName'])
    print(stock_stats['sharesOutstanding'])
    print('Date\tOpen\tHigh\tLow\tClose\tVolume\tIndicator\tBuy?\tSell?')

    for chart in stock_chart:

        # formatting purposes to prevent program from crashing
        if indicator_list[index] is not None and type(indicator_list[index]) is float:
            indicator = f"{indicator_list[index]:.4f}"
        elif type(indicator_list[index]) is int:
            if  indicator_list[index] > 0:
                indicator = '+' + str(indicator_list[index])
            else:
                indicator = str(indicator_list[index])
        else:
            indicator = ""

        # print output in tab-delimited format --- All stock inforamtion is below
        print("{}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{}\t{}\t{}\t{}".format(
            chart['date'], chart['open'],
            chart['high'], chart['low'],
            chart['close'], chart['volume'],
            indicator, buy_sell[index][0],
            buy_sell[index][1])
        )
        index += 1

    # license
    print("Data provided for free by IEX")
    print("View IEX's Terms of Use")
    print("https://iextrading.com/api-exhibit-a/")


'''Runs all necessary commands to run program successfully'''
def run() -> None:

    # Gathers user input
    userInput = _user_input()
    symbolInput = userInput[0]
    dayInput = userInput[1]
    strategyInput = userInput[2]

    # gathers stock info
    stockInfo = pdi.request_stock_info(pdi.build_search_url(symbolInput, dayInput))
    stockChart = stockInfo[symbolInput.upper()]['chart']

    # keeps only the information needed
    x = len(stockChart) - dayInput
    while x != 0:
        stockChart.pop(0)
        x -= 1

    # storing indicator and signal strategy information needed to print
    indicatorList = []
    indicatorDataList = []
    sigstratList = []
    for index in range(dayInput):
        # INDICATORS
        indicatorObject = _create_indicator(strategyInput)
        indiVal, indiStoredData = _store_indicator_info(stockChart, index, indicatorObject, userInput)
        indicatorList.append(indiVal)
        indicatorDataList.append(indiStoredData)

    for index in range(dayInput):
        # SIGNAL STRATEGIES
        sigstratObject = _create_signal_strategy(strategyInput)
        buySell = _store_signal_strategy(indicatorDataList, indicatorList, sigstratObject, index)
        sigstratList.append(buySell)

    # output information
    _print_stock_info(stockInfo, indicatorList, sigstratList, symbolInput)


'''runs if module is main'''
if __name__ == '__main__':
    run()