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
    i = 0 if (size - windowSize < 0) else size - windowSize
    for i in range(0, size):
        x = nTransactionsTreated[i] - micro
        total += x * x

    delta = math.sqrt(total / (n - 1))
    return delta

# Params:
# - (Int) nTransactionsTreated: Integer representing the number of treated transactions in one second;
# - (Int) nTransactionsRequested: Integer representing the number of requested transactions in the same second;
def calculateTransactionTroughput(nTransactionsTreated, nTransactionsRequested):
    if nTransactionsRequested == 0:
        return 0.0
    return nTransactionsTreated / nTransactionsRequested

# Params:
# - (Float array) x: Array containing time data (X axis)
# - (Float array) y: Array containing transactionsTreated data (Y axis)
def calculatePerformanceTrend(x, y, windowSize, debug):
    if len(x) != len(y):
        print('Calculating performanceTrend with two arrays of different size... Aborting...')
        return

    size = min(windowSize, len(x))

    if debug:
        print('Size is ' + str(size))

    # array[-size:] gives us the last <size> elements of the array
    npx = np.array(x[-size:])
    npy = np.array(y[-size:])

    if debug:
        print('Npx size ' + str(len(npx)))
        print('Npy size ' + str(len(npy)))

    # Use least squares to find (a, b) so that f(x) = ax + b. Returns array [a,b].
    z = np.polyfit(npx, npy, 1)
    # Create function in python that implements the f(x) obtained in the last command
    fx = np.poly1d(z) # now, if i want to calculate where x = 0.5, just do fx(0.5)

    if debug:
        print("f(x) = (" + str(z[0]) + ") * x + (" + str(z[1]) + ")")



    # Print correct values vs generated function
    # for i in range(0, len(x)):
    #    print("f(" + str(i) + ") = '" + str(fx(i)) + "', correct is " + str(y[i]))

    decrescent = z[0] < 0

    if decrescent:
        root = fx.r # calculate x'

        if debug:
            print('Decrescent, root is ' + str(root) + '\n')

        # print("its 0 when...")
        # print(root)
        # print(fx(root))

        return root - x[len(x)-1]

    if debug:
        print('Crescent function.\n')

    return None

# Construct the polynomial x^2 + 2x + 3:

#>>> p = np.poly1d([1, 2, 3])
#>>> print(np.poly1d(p))
#   2
#1 x + 2 x + 3
#Evaluate the polynomial at x = 0.5:

#>>> p(0.5)
#4.25
