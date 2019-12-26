# main purpose of module is to stores data in the classes
# generates a signal strategy for the user


# calculates True Range signal strategy
class TRCalc:


    '''initialize variables'''
    def __init__(self) -> None:
        self._sigstratStrBuy = ''
        self._sigstratStrSell = ''


    '''Conditions for signal strategy: caculates signal strategy'''
    def calculate(self, indicatorDataList: list, indiValList: list, index: int) -> tuple:
        indicatorData = indicatorDataList[index]
        indiVal = indiValList[index]
        buyThresh = indicatorData[0]
        sellThresh = indicatorData[1]

        # makes sure there is indicatorData to calculate
        if indiVal is not None:
            if buyThresh.startswith('<'):
                if indiVal < float(buyThresh[1:]):
                    self._sigstratStrBuy = 'BUY'
            elif buyThresh.startswith('>'):
                if indiVal > float(buyThresh[1:]):
                    self._sigstratStrBuy = 'BUY'
            else:
                self._sigstratStrBuy = ''

            if sellThresh.startswith('>'):
                if indiVal > float(sellThresh[1:]):
                    self._sigstratStrSell = 'SELL'
            elif sellThresh.startswith('<'):
                    if indiVal < float(buyThresh[1:]):
                        self._sigstratStrBuy = 'BUY'
            else:
                self._sigstratStrSell = ''

        return self._sigstratStrBuy, self._sigstratStrSell


# calculates Simple Moving Average Price signal strategy
class MPCalc:


    '''initialize variables'''
    def __init__(self) -> None:
        self._sigstratStrBuy = ''
        self._sigstratStrSell = ''


    '''Conditions for signal strategy: caculates signal strategy'''
    def calculate(self, indicatorDataList: list, indiValList: list, index: int) -> tuple:

        indiVal = indiValList[index]
        indicatorData = indicatorDataList[index]
        current_price = indicatorData[0]
        previous_price = indicatorData[1]
        if indiValList[index - 1] is not None:
            previous_indicator = indiValList[index - 1]
        else:
            previous_indicator = None

        # makes sure there is an indicator data to calculate as well as a previous indicator
        if indiVal is not None and previous_indicator is not None:
            if indiVal < current_price and previous_indicator > previous_price:
                self._sigstratStrBuy = 'BUY'
            elif indiVal > current_price and previous_indicator < previous_price:
                self._sigstratStrSell = 'SELL'
            else:
                self._sigstratStrBuy = ''
                self._sigstratStrSell = ''
        else:
            self._sigstratStrBuy = ''
            self._sigstratStrSell = ''

        return self._sigstratStrBuy, self._sigstratStrSell


# calculates Simple Moving Average Volume signal strategy
class MVCalc:


    '''initialize variables'''
    def __init__(self) -> None:
        self._sigstratStrBuy = ''
        self._sigstratStrSell = ''
        self._volume_indicator = 0


    '''Conditions for signal strategy: caculates signal strategy'''
    def calculate(self, indicatorDataList: list, indiValList: list, index: int) -> tuple:

        indiVal = indiValList[index]
        indicatorData = indicatorDataList[index]
        current_volume = indicatorData[0]
        previous_volume = indicatorData[1]
        if indiValList[index - 1] is not None:
            previous_indicator = indiValList[index - 1]
        else:
            previous_indicator = None

            # makes sure there is an indicator data to calculate as well as a previous indicator
        if indiVal is not None and previous_indicator is not None:
            if indiVal < current_volume and previous_indicator > previous_volume:
                self._sigstratStrBuy = 'BUY'
            elif indiVal > current_volume and previous_indicator < previous_volume:
                self._sigstratStrSell = 'SELL'
            else:
                self._sigstratStrBuy = ''
                self._sigstratStrSell = ''
        else:
            self._sigstratStrBuy = ''
            self._sigstratStrSell = ''

        return self._sigstratStrBuy, self._sigstratStrSell


# calculates Directional Indicator Price signal strategy
class DPCalc:


    '''initialize variables'''
    def __init__(self) -> None:
        self._sigstratStrBuy = ''
        self._sigstratStrSell = ''
        self._direction_indicator = 0


    '''Conditions for signal strategy: caculates signal strategy'''
    def calculate(self, indicatorDataList: list, indiValList: list, index: int) -> tuple:

        indicatorData = indicatorDataList[index]
        indiVal = indiValList[index]
        buyThresh = indicatorData[0]
        sellThresh = indicatorData[1]

        # calculates the directional indicator for price
        if index - 1 >= 0:

            if buyThresh.startswith('+'):
                if indiVal > int(buyThresh[1:]) >= indiValList[index - 1]:
                    self._sigstratStrBuy = 'BUY'
            else:
                if indiVal > int(buyThresh) >= indiValList[index - 1]:
                    self._sigstratStrBuy = 'BUY'

            if sellThresh.startswith('+'):
                if indiVal < int(sellThresh[1:]) <= indiValList[index - 1]:
                    self._sigstratStrSell = 'SELL'
            else:
                if indiVal < int(sellThresh) <= indiValList[index - 1]:
                    self._sigstratStrSell = 'SELL'

        return self._sigstratStrBuy, self._sigstratStrSell


# calculates Directional Indicator Volume signal strategy
class DVCalc:


    '''initialize variables'''
    def __init__(self) -> None:
        self._sigstratStrBuy = ''
        self._sigstratStrSell = ''
        self._direction_indicator = 0


    '''Conditions for signal strategy: caculates signal strategy'''
    def calculate(self, indicatorDataList: list, indiValList: list, index: int) -> tuple:

        indicatorData = indicatorDataList[index]
        indiVal = indiValList[index]
        buyThresh = indicatorData[0]
        sellThresh = indicatorData[1]

        # calculates the directional indicator for volume
        if index - 1 >= 0:

            if buyThresh.startswith('+'):
                if indiVal > int(buyThresh[1:]) >= indiValList[index - 1]:
                    self._sigstratStrBuy = 'BUY'
            else:
                if indiVal > int(buyThresh) >= indiValList[index - 1]:
                    self._sigstratStrBuy = 'BUY'

            if sellThresh.startswith('+'):
                if indiVal < int(sellThresh[1:]) <= indiValList[index - 1]:
                    self._sigstratStrSell = 'SELL'
            else:
                if indiVal < int(sellThresh) <= indiValList[index - 1]:
                    self._sigstratStrSell = 'SELL'

        return self._sigstratStrBuy, self._sigstratStrSell
