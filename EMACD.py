import pandas as pd
import numpy as np
import math


data = pd.read_csv('data.csv')


def exponentialMovingAverage(expFactor, shortTermLength, LongTermLength):
    shortTermWeights = []
    longTermWeights = []

    workingCapital = 1000000
    cashAvailable = workingCapital

    shortMovingAverage = 0
    longMovingAverage = 0

    for i in range(0, LongTermLength):
        if( i < shortTermLength):
            shortTermWeights.append(math.exp(expFactor * i))
        longTermWeights.append(math.exp(expFactor * i))

    shortTermTotalWeight = sum(shortTermWeights)
    longTermTotalWeight = sum(longTermWeights)

    for i in range(0, LongTermLength):
        if( i < shortTermLength):
            shortTermWeights[i] = (shortTermWeights[i] / shortTermTotalWeight)
        longTermWeights[i] = (longTermWeights[i] / longTermTotalWeight)


    prices = data['Price'].to_list()


    numUnits = 0
    for i in range(LongTermLength, len(prices)):
        longMovingAverage = (np.dot(prices[i - LongTermLength:i], longTermWeights))
        shortMovingAverage = (np.dot(prices[i-shortTermLength:i], shortTermWeights))
        difference = shortMovingAverage - longMovingAverage
        if( difference >  0):
            if(numUnits == 0):
                numUnits = math.floor(cashAvailable / prices[i])
                cashAvailable -= numUnits * prices[i]
        elif( difference <  0 or i == len(prices) - 1):
            if(numUnits != 0):
                cashAvailable += numUnits * prices[i]
                numUnits = 0

    totalReturn = (cashAvailable - workingCapital) / workingCapital
    bmark = (data['Price'][len(prices) - 1] - data['Price'][LongTermLength]) /  data['Price'][LongTermLength]
    print('Benchmark return: ' + str(bmark))
    print('Total return: ' + str(totalReturn))

    if( totalReturn > bmark):
        print("WE BEAT THE MARKET")




if __name__ == "__main__":
    exponentialMovingAverage(0.2, 12, 26)