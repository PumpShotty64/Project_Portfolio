# main purpose of module is to stores data in the classes
# creates an indicator for user to see


# produces a True Range object class
class TrueRange:

    '''initialize variables for use and to store'''
    def __init__(self) -> None:
        self._buy_thresh = 0
        self._sell_thresh = 0
        self._max_price = 0
        self._min_price = 0
        self._previous_price = None


    '''stores the data needed to calculate indicator and generate signal strategy'''
    def store_data(self, chartsDict: dict, index:int, userInput: tuple) -> tuple:

        # gathers info from parameters
        inputInfo = userInput[2]
        action, buyThresh, sellThresh = inputInfo.split()
        currentChart = chartsDict[index]

        # sets variable of previous chart information if it exists
        if index != 0:
            previousChart = chartsDict[index - 1]
        else:
            previousChart = None

        self._buy_thresh = buyThresh
        self._sell_thresh = sellThresh

        # sets max and min prices and stores information for signal strategy
        if previousChart is not None:
            self._previous_price = previousChart['close']

            if currentChart['high'] >= previousChart['close']:
                self._max_price = currentChart['high']
            else:
                self._max_price = previousChart['close']

            if currentChart['low'] <= previousChart['close']:
                self._min_price = currentChart['low']
            else:
                self._min_price = previousChart['close']
        else:
            self._max_price = currentChart['high']
            self._min_price = currentChart['low']

        return self._buy_thresh, self._sell_thresh


    '''caculates indicator'''
    def generate(self) -> float:
        if self._previous_price is not None:
            return float((self._max_price - self._min_price)/self._previous_price * 100)


# produces a Simple Moving Average object class for Price
class SimpleMovingAveragePrice:


    '''intialize variables'''
    def __init__(self) -> None:
        self._num_days = 0
        self._closing_price = 0
        self._accumulated_price = 0
        self._price_indicator = 0
        self._previous_price = None


    '''stores the data needed to calculate indicator and generate signal strategy'''
    def store_data(self, chartsDict: dict, index:int, userInput: tuple) -> tuple:

        # gathers info from parameters
        inputInfo = userInput[2]
        action, numDays = inputInfo.split()
        currentChart = chartsDict[index]

        # sets variable of previous chart information if it exists
        if index != 0:
            previousChart = chartsDict[index - 1]
        else:
            previousChart = None

        self._num_days = int(numDays)
        self._closing_price = currentChart['close']

        if previousChart is not None:
            self._previous_price = previousChart['close']

        # calculates accumulated price if there is sufficient data
        for i in range(int(numDays)):
            if index - i >= 0:
                self._accumulated_price += chartsDict[index - i]['close']
            else:
                self._accumulated_price = None
                break

        return self._closing_price, self._previous_price


    '''caculates indicator'''
    def generate(self) -> float:
        try:
            self._price_indicator = self._accumulated_price / self._num_days
        except TypeError:
            self._price_indicator = None

        return self._price_indicator


# produces a Simple Moving Average object class for Volume
class SimpleMovingAverageVolume:


    '''intialize variables'''
    def __init__(self) -> None:
        self._num_days = 0
        self._volume = 0
        self._accumulated_volume = 0
        self._volume_indicator = 0
        self._previous_volume = None


    '''stores the data needed to calculate indicator and generate signal strategy'''
    def store_data(self, chartsDict: dict, index:int, userInput: tuple) -> tuple:

        # gathers info from parameters
        inputInfo = userInput[2]
        action, numDays = inputInfo.split()
        currentChart = chartsDict[index]

        # sets variable of previous chart information if it exists
        if index != 0:
            previousChart = chartsDict[index - 1]
        else:
            previousChart = None

        self._num_days = int(numDays)
        self._volume = currentChart['volume']

        if previousChart is not None:
            self._previous_volume = previousChart['volume']

        # calculates accumulated volume if there is sufficient data
        for i in range(int(numDays)):
            if index - i >= 0:
                self._accumulated_volume += chartsDict[index - i]['volume']
            else:
                self._accumulated_volume = None

        return self._volume, self._previous_volume


    '''caculates indicator'''
    def generate(self) -> float:
        try:
            self._volume_indicator = self._accumulated_volume / self._num_days
        except TypeError:
            self._volume_indicator = None

        return self._volume_indicator


# produces a Directional Indicator for Price
class DirectionalIndicatorPrice:


    '''intialize variables'''
    def __init__(self) -> None:
        self._buy_thresh = 0
        self._sell_thresh = 0
        self._direction_counter = 0

    '''stores the data needed to calculate indicator and generate signal strategy'''
    def store_data(self, chartsDict: dict, index:int, userInput: tuple) -> tuple:

        # declare variables
        positive_count = 0
        negative_count = 0

        # gathers info from parameters
        inputInfo = userInput[2]
        action, numDays, buyThresh, sellThresh = inputInfo.split()

        self._buy_thresh = buyThresh
        self._sell_thresh = sellThresh

        # calculates directional counter by adding or subtracting one dependent on prices
        for i in range(int(numDays)):
            if index - i - 1 >= 0:
                if chartsDict[index - i]['close'] > chartsDict[index - i - 1]['close']:
                    positive_count += 1
                elif chartsDict[index - i]['close'] < chartsDict[index - i - 1]['close']:
                    negative_count += 1

        self._direction_counter = positive_count - negative_count

        return self._buy_thresh, self._sell_thresh


    '''caculates indicator'''
    def generate(self) -> int:
        return int(self._direction_counter)


# produces a Directional Indicator for Volume
class DirectionalIndicatorVolume:


    '''intialize variables'''
    def __init__(self) -> None:
        self._buy_thresh = 0
        self._sell_thresh = 0
        self._direction_counter = 0


    '''stores the data needed to calculate indicator and generate signal strategy'''
    def store_data(self, chartsDict: dict, index:int, userInput: tuple) -> tuple:

        # declare variables
        positive_count = 0
        negative_count = 0

        # gathers info from parameters
        inputInfo = userInput[2]
        action, numDays, buyThresh, sellThresh = inputInfo.split()

        self._buy_thresh = buyThresh
        self._sell_thresh = sellThresh

        # calculates directional counter by adding or subtracting one dependent on volumes
        for i in range(int(numDays)):
            if index - i - 1 >= 0:
                if chartsDict[index - i]['volume'] > chartsDict[index - i - 1]['volume']:
                    positive_count += 1
                elif chartsDict[index - i]['volume'] < chartsDict[index - i - 1]['volume']:
                    negative_count += 1

        self._direction_counter = positive_count - negative_count

        return self._buy_thresh, self._sell_thresh


    '''caculates indicator'''
    def generate(self) -> int:
        return int(self._direction_counter)