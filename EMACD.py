import pandas as pd
import numpy as np
import math

# Calculates day weightings according to the formula exp(tbV/10^9)
def volumeBasedWeights(length, b, volumes):
    weights = []
    for t in range(0, length):
        weights.append(math.exp(t*b*(volumes[t] / 1000000000)))
    weightSum = sum(weights)
    for t in range(0, length):
        weights[t] = weights[t] / weightSum
    return weights


def movingAverage(shortTermLength, LongTermLength, volumeFactor):

    # Loading initial variables
    shortMovingAverage = 0
    longMovingAverage = 0
    workingCapital = 1000000
    cashAvailable = workingCapital
    cash = []
    numTrades = 0
    numUnits = 0

    # Converting price and volume information to a list
    prices = data['Price'].to_list()
    volumes = data['Volume'].to_list()

    # Looping through the time period
    for i in range(LongTermLength, len(prices)):
        #  Calculate the weights for both periods
        shortTermWeights = volumeBasedWeights(shortTermLength, volumeFactor, volumes[i - shortTermLength:i])
        longTermWeights = volumeBasedWeights(LongTermLength, volumeFactor, volumes[i - LongTermLength:i])

        # Calclate the averages from the weights and prices
        longMovingAverage = (np.dot(prices[i - LongTermLength:i], longTermWeights))
        shortMovingAverage = (np.dot(prices[i - shortTermLength:i], shortTermWeights))

        difference = shortMovingAverage - longMovingAverage

        # Buy and selling conditions
        if( difference >  0):
            if(numUnits == 0):
                numUnits = math.floor(cashAvailable / (prices[i]))
                cashAvailable -= numUnits * (prices[i])
                numTrades += 1
        if( difference <  0 or i == len(prices) - 1):
            if(numUnits != 0):
                cashAvailable += numUnits * (prices[i])
                numUnits = 0
                numTrades += 1
        # Collect portfolio value information
        cash.append(numUnits * (prices[i]) + cashAvailable)
    #  Calculate total return
    totalReturn = (cashAvailable - workingCapital) / workingCapital
    #  Calculate benchmark returns
    bmark = (data['Price'][len(prices) - 1] - data['Price'][LongTermLength]) /  data['Price'][LongTermLength]
    print(bmark)
    print(totalReturn)


if __name__ == "__main__":
    data = pd.read_csv('data/2017-2020-withVolume.csv')
    movingAverage(12, 26, 2.88)

    