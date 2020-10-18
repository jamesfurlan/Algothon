import pandas as pd
import numpy as np
import math


data = pd.read_csv('data.csv')


shortTermWeights = []
longTermWeights = []

shortTermLength = 12
LongTermLength = 26
expFactor = 0.2

shortMovingAverage = 0
longMovingAverage = 0


i = 0

while i < LongTermLength:
    if( i < shortTermLength):
        shortTermWeights.append(math.exp(expFactor * i))
    longTermWeights.append(math.exp(expFactor * i))
    i += 1

shortTermTotalWeight = sum(shortTermWeights)
longTermTotalWeight = sum(longTermWeights)

i = 0
while i < LongTermLength:
    if( i < shortTermLength):
        shortTermWeights[i] = (shortTermWeights[i] / shortTermTotalWeight)
    longTermWeights[i] = (longTermWeights[i] / longTermTotalWeight)
    i += 1 


i = LongTermLength
prices = data['Price'].to_list()
while i < len(prices):
    longMovingAverage = (np.dot(prices[i - LongTermLength:i], longTermWeights))
    shortMovingAverage = (np.dot(prices[i-shortTermLength:i], shortTermWeights))
    difference = shortMovingAverage - longMovingAverage
    if( difference >  0):
        print('Buy on: ' + data['Date'][i])
    elif( difference <  0):
        print('Sell on: ' + data['Date'][i])
    i += 1

