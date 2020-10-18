import pandas as pd
import numpy as np
import math
from weightType import WeightType
from matplotlib import pyplot as plt


data = pd.read_csv('2010-2020.csv')




def exponentialWeights(factor, length):
    weights = []
    for i in range(0, length):
        weights.append(math.exp(factor * i))
    weightSum = sum(weights)
    for i in range(0, length):
        weights[i] = weights[i] / weightSum
    return weights

# def linearWeights(factor, length):
#     weights = []
#     for i in range(0, length):
#         weights.append(factor * i)
#     weightSum = sum(weights)
#     for i in range(0, length):
#         weights[i] = weights[i] / weightSum
#     return weights



# def flatWeights(length):
#     weights = []
#     for i in range(0, length):
#         weights.append(1 / length)
#     assert(sum(weights) == 1)
#     return weights


def movingAverage(factor, shortTermLength, LongTermLength, weightType):
    if (weightType == WeightType.EXPONENTIAL):
        shortTermWeights = exponentialWeights(factor, shortTermLength)
        longTermWeights = exponentialWeights(factor, LongTermLength)
    # elif (weightType == WeightType.FLAT):
    #     shortTermWeights = flatWeights(shortTermLength)
    #     longTermWeights = flatWeights(LongTermLength)
    # elif (weightType == WeightType.LINEAR):
    #     shortTermWeights = linearWeights(factor, shortTermLength)
    #     longTermWeights = linearWeights(factor, LongTermLength)

    workingCapital = 1000000
    cashAvailable = workingCapital

    shortMovingAverage = 0
    longMovingAverage = 0


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
        if( difference <  0 or i == len(prices) - 1):
            if(numUnits != 0):
                cashAvailable += numUnits * prices[i]
                numUnits = 0

    totalReturn = (cashAvailable - workingCapital) / workingCapital
    bmark = (data['Price'][len(prices) - 1] - data['Price'][LongTermLength]) /  data['Price'][LongTermLength]
    # print(bmark)
    return totalReturn
    # if( totalReturn > bmark):
    #     print('\nBenchmark return: ' + str(bmark))
    #     print('Total return: ' + str(totalReturn))
    #     print('factor: ' + str(factor)+ ' type: ' + str(weightType))
    #     print("WE BEAT THE MARKET\n")




if __name__ == "__main__":
    returns = []
    factors = []
    # Factor checks
    for i in range(1, 300):
        factors.append(i / 100)
        returns.append(movingAverage(i / 100, 50, 200, WeightType.EXPONENTIAL))
    plt.xlabel('Exponential weightings')
    plt.ylabel('Returns')
    plt.plot(factors, returns)
    plt.savefig('factorReturns.png')

    