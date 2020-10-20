import pandas as pd
import numpy as np
import math
from weightType import WeightType
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d


# data = pd.read_csv('2015-2020-withVolume.csv')




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

def volumeBasedWeights(a, length, b, volumes):
    weights = []
    for t in range(0, length):
        weights.append(math.exp(t*b*(volumes[t] / 1000000000)))
    weightSum = sum(weights)
    for i in range(0, length):
        weights[i] = weights[i] / weightSum
    return weights


def movingAverage(factor, shortTermLength, LongTermLength, weightType, volumeFactor):
    # if (weightType == WeightType.EXPONENTIAL):
        # shortTermWeights = exponentialWeights(factor, shortTermLength, volumeFactor, volumes[i])
        # longTermWeights = exponentialWeights(factor, LongTermLength, volumeFactor, volumes[i])
    # elif (weightType == WeightType.FLAT):
    #     shortTermWeights = flatWeights(shortTermLength)
    #     longTermWeights = flatWeights(LongTermLength)
    # elif (weightType == WeightType.LINEAR):
    #     shortTermWeights = linearWeights(factor, shortTermLength)
    #     longTermWeights = linearWeights(factor, LongTermLength)


    shortMovingAverage = 0
    longMovingAverage = 0


    prices = data['Price'].to_list()
    volumes = data['Volume'].to_list()

    workingCapital = 1000000
    cashAvailable = workingCapital

    # for i in range(0, len(volume)):
    #     volumeWeights.append(math.exp(factor + volumeFactor * ( volumes[i] / 1000000000))

    cash = []
    numTrades = 0
    numUnits = 0
    boringUnits = math.floor(cashAvailable / prices[LongTermLength])
    boring = []
    for i in range(LongTermLength, len(prices)):
        shortTermWeights = volumeBasedWeights(factor, shortTermLength, volumeFactor, volumes[i - shortTermLength:i])
        longTermWeights = volumeBasedWeights(factor, LongTermLength, volumeFactor, volumes[i - LongTermLength:i])
        # print(shortTermWeights)
        # print(longTermWeights)
        longMovingAverage = (np.dot(prices[i - LongTermLength:i], longTermWeights))
        shortMovingAverage = (np.dot(prices[i-shortTermLength:i], shortTermWeights))
        difference = shortMovingAverage - longMovingAverage
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
        cash.append(numUnits * (prices[i]) + cashAvailable)
        boring.append(boringUnits * prices[i])
    # print(numTrades)
    plt.plot(data['Date'].to_list()[LongTermLength:], cash,'r', data['Date'].to_list()[LongTermLength:], boring,'b')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Capital for 2017-2020 with factor 2.88')
    plt.savefig('Capital_2.88.png')
    plt.close()
    totalReturn = (cashAvailable - workingCapital) / workingCapital
    bmark = (data['Price'][len(prices) - 1] - data['Price'][LongTermLength]) /  data['Price'][LongTermLength]
    print(bmark)
    return totalReturn
    # if( totalReturn > bmark):
    #     print('\nBenchmark return: ' + str(bmark))
    #     print('Total return: ' + str(totalReturn))
    #     print('factor: ' + str(factor)+ ' type: ' + str(weightType))
    #     print("WE BEAT THE MARKET\n")




if __name__ == "__main__":
    data = pd.read_csv('2017-2020-withVolume.csv')
    returns = []
    a_factors = []
    b_factors = []
    maxReturn = 0
    maxExponent = 0
    # Factor checks
    # for a in range(0, 10):
    #     A = []
    #     a_factors.append(a / 10)
    #     b_factors.append(a / 10)
    # for b in range(0, 700):
    #     b_factors.append(b / 100) 
    result = movingAverage(0.26, 12, 26, WeightType.EXPONENTIAL, 2.88)
    #     returns.append(result)
    #     if result > maxReturn:
    #         maxReturn = result
    #         maxExponent = b/100
    # print(maxExponent)
    # returns.append(A)

    # prices = data['Price'].to_list()
    # bmark = (data['Price'][len(prices) - 1] - data['Price'][26]) /  data['Price'][26]
    # bmark_array = []
    # for i in range(0, len(b_factors)): bmark_array.append(bmark)
    # plt.plot(b_factors, returns, 'b', b_factors, bmark_array, 'r--')
    # plt.xlabel('exponential decay factors')
    # plt.ylabel('Returns')
    # plt.title('Returns for different exponential decay factors')
    # plt.savefig('returnsToB.png')
    # print(maxReturn)

    # a, b = np.meshgrid(a_factors, b_factors)

    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.contour3D(a, b, returns, 50, cmap='binary')
    # ax.set_xlabel('a weightings')
    # ax.set_ylabel('b weightings')
    # ax.set_zlabel('Returns')
    # plt.savefig('3DtwoFactorReturns.png')

    