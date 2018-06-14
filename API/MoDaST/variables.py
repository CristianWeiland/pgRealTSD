import math
import numpy as np

# Params:
# - (Int) n: number of observations
# - (Int array) nTransactionsTreated: Array of ints representing the number of treated transactions in that second;
# - (Int) windowSize: how many elements from nTransactionsTreated we will use to calculate the performanceVariation.
def calculatePerformanceVariation(n, nTransactionsTreated, windowSize):
    if n <= 1:
        return 0

    micro = sum(nTransactionsTreated) / n

    size = len(nTransactionsTreated)
    total = 0.0
    if size - windowSize < 0:
        init = 0
    else:
        init = size - windowSize

    for i in range(init, size):
        x = nTransactionsTreated[i] - micro
        total += x * x

    delta = math.sqrt(total / (n - 1))
    return delta

# Params:
# - (Int) nTransactionsTreated: Integer representing the number of treated transactions in one second;
# - (Int) nTransactionsRequested: Integer representing the number of requested transactions in the same second;
def calculateTransactionTroughput(nTransactionsTreated, nTransactionsRequested, windowSize):
    # Uncomment this if we want to look to only this instant
    # if nTransactionsRequested == 0:
    #     return 0.0
    # return nTransactionsTreated / nTransactionsRequested

    size = len(nTransactionsTreated)
    if size - windowSize < 0:
        init = 0
    else:
        init = size - windowSize

    totalTreated = 0
    totalRequested = 0
    for i in range(init, size):
        totalTreated += nTransactionsTreated[i]
        totalRequested += nTransactionsRequested[i]

    if totalRequested == 0:
        return 0.0
    return totalTreated / totalRequested

# Params:
# - (Float array) x: Array containing time data (X axis)
# - (Float array) y: Array containing transactionsTreated data (Y axis)
def calculatePerformanceTrend(x, y, windowSize):
    if len(x) != len(y):
        print('Calculating performanceTrend with two arrays of different size... Aborting...')
        return None

    if len(x) == 1:
        return None

    size = min(windowSize, len(x))

    # array[-size:] gives us the last <size> elements of the array
    npx = np.array(x[-size:])
    npy = np.array(y[-size:])

    # Use least squares to find (a, b) so that f(x) = ax + b. Returns array [a,b].
    z = np.polyfit(npx, npy, 1)
    # Create function in python that implements the f(x) obtained in the last command
    fx = np.poly1d(z) # now, if i want to calculate where x = 0.5, just do fx(0.5)

    decrescent = z[0] < 0

    if decrescent:
        root = fx.r # calculate x'

        if len(root) == 0:
            return None
        return root[0] - x[len(x)-1]

    return None
