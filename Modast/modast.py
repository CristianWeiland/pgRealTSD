import json
import argparse
import variables # ./variables.py
import states # ./states.py
from pprint import pprint

parser = argparse.ArgumentParser(description='Modast in python.')

parser.add_argument('-f', '--filename', action="store", dest="filename",
            help="[str] name of the JSON file containing data", default="data.json")
parser.add_argument('-nt', '--normalize', action="store", dest="normalize",
            help="[str true/false], if we should or not normalize time", default="true")
parser.add_argument('-w', '--window', action="store", dest="windowSize",
            help="[int] window size, -1 = infinity", default="-1")

args = parser.parse_args()

with open(args.filename) as f:
    data = json.load(f)

time = []
normalizedTime = []
treated = []
requested = []
for key in data:
	time.append(int(key))
	treated.append(int(data[key]['responses']))
	requested.append(int(data[key]['requests']))

# At this moment, we created an array from each value from the JSON, but this is not sorted.
# We need to sort the 3 arrays at the same time, using Time array as the key.
# To do so, we will first zip them, created an array of touples:
# [ (time[0], treated[0], requested[0]), ..., (time[n], treated[n], requested[n]) ]

zipped = zip(time, treated, requested)
# Then, sort it
sort = sorted(zipped, key=lambda pair: pair[0])

# Now, split into three different arrays:
timeSorted = [a for a, b, c in sort]
treatedSorted = [b for a, b, c in sort]
requestedSorted = [c for a, b, c in sort]

# Normalize time:
if args.normalize == 'true':
    minimum = timeSorted[0] - 1 # -1 to make sure we wont have 0 seconds as time
    timeSorted = [x - minimum for x in timeSorted]

windowSize = int(args.windowSize)
if windowSize == -1: # Use every data we have
    windowSize = len(timeSorted)

currentState = states.initialState

# We will simulate receiving data here. So, we will calculate states using
# arrays of length 1, length 2, ..., length len(timeSorted)
for i in range(0, len(timeSorted)):
    # First, slice arrays so we dont have data from the future
    partialTime = timeSorted[:i+1]
    partialTreated = treatedSorted[:i+1]
    partialRequested = requestedSorted[:i+1]

    performanceVariation = variables.calculatePerformanceVariation(i, partialTreated, windowSize)
    # transactionTroughput only looks to current second, so we dont need windowSize
    transactionTroughput = variables.calculateTransactionTroughput(partialTreated[i], partialRequested[i])
    performanceTrend = variables.calculatePerformanceTrend(partialTime, partialTreated, windowSize)

    currentState = states.getNextState(currentState, performanceVariation, transactionTroughput, performanceTrend, partialTreated[i])

    print('+-----------------------------------------------------------+')
    print('| Iteration #' + str(i) + "\n|")
    print('| Performance Variation: ' + str(performanceVariation))
    print('| Transaction Troughput: ' + str(transactionTroughput))
    print('| Performance Trend: ' + str(performanceTrend))
    print('| Current State: ' + str(currentState))
    print('+-----------------------------------------------------------+\n')

# performanceTrend = variables.calculatePerformanceTrend(timeSorted, treatedSorted)
# print(performanceTrend)

