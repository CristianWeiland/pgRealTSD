# Libraries
import json
import time
import numpy as np
import argparse
import datetime
import matplotlib.pyplot as plt
from pprint import pprint

# Local Imports
import variables # ./variables.py
import states # ./states.py

def is_Power(x, y):
    if (x == 0):
        return False
    while (x % y == 0):
        x = x / y
    return x == 1

parser = argparse.ArgumentParser(description='Modast in python.')

parser.add_argument('-f', '--filename', action="store", dest="filename",
            help="[str] name of the JSON file containing data. Default = data.json.", default="data.json")
parser.add_argument('-nt', '--normalize', action="store", dest="normalize",
            help="[str true/false], if we should or not normalize time. Default = true.", default="true")
parser.add_argument('-w', '--window', action="store", dest="windowSize",
            help="[int] window size, -1 = infinity. Default = -1.", default="-1")
parser.add_argument('-ppt', '--printperformancetrend', action="store", dest="ppt",
            help="[str true/false] debug performance trend or not. Default = false.", default="false")
parser.add_argument('-plot', '--plot', action="store", dest="plot",
            help="[str true/false] plot results. Default = true.", default="true")
parser.add_argument('-s', '--save', action="store", dest="save",
            help="[str true/false] save results in png file instead of showing them. Default = false.", default="false")
parser.add_argument('-o', '--output', action="store", dest="output",
            help="[str true/false] output filename. Only works if save = true.", default="false")
parser.add_argument('-d', '--output_dir', action="store", dest="output_dir",
            help="[str true/false] output dir.", default="./")
parser.add_argument('-separate', '--separatedwindows', action="store", dest="separate",
            help="[str true/false] separate into 4 graph windows. Default = false.", default="false")

args = parser.parse_args()

ppt = args.ppt == 'true'

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
minimum = 0
if args.normalize == 'true':
    minimum = timeSorted[0] - 1 # -1 to make sure we wont have 0 seconds as time
    timeSorted = [x - minimum for x in timeSorted]

windowSize = int(args.windowSize)
if windowSize == -1: # Use every data we have
    windowSize = len(timeSorted)

currentState = states.initialState

# We will simulate receiving data here. So, we will calculate states using
# arrays of length 1, length 2, ..., length len(timeSorted)
finalPV = []
finalTT = []
finalPT = []
finalCS = []
xPlot = []
for i in range(0, len(timeSorted)):
    initialTime = datetime.datetime.now()

    # First, slice arrays so we dont have data from the future
    partialTime = timeSorted[:i+1]
    partialTreated = treatedSorted[:i+1]
    partialRequested = requestedSorted[:i+1]

    performanceVariation = variables.calculatePerformanceVariation(i, partialTreated, windowSize)
    # uncomment this if we want transactionTroughput to consider only this second
    # transactionTroughput = variables.calculateTransactionTroughput(partialTreated[i], partialRequested[i], windowSize)
    # uncomment this if we want transactionTroughput to consider the whole window
    transactionTroughput = variables.calculateTransactionTroughput(partialTreated, partialRequested, windowSize)
    #performancetrend = variables.calculateperformancetrend(partialtime, partialtreated, windowsize, ppt)
    performanceTrend = variables.calculatePerformanceTrend(partialTime, partialTreated, windowSize)

    currentState = states.getNextState(currentState, performanceVariation, transactionTroughput, performanceTrend, partialTreated[i])

    finalPV.append(performanceVariation)
    finalTT.append(transactionTroughput)
    finalPT.append(performanceTrend)
    finalCS.append(currentState)
    xPlot.append(i)

    finalTime = datetime.datetime.now()
    if is_Power(i, 2) or i == (len(timeSorted) -1):
        delta = finalTime - initialTime
        #print("Time spent with i = " + str(i) + ": " + str(delta.total_seconds()))

    """
    print('+-----------------------------------------------------------+')
    print('| Iteration #' + str(i) + "\n|")
    print('| Timestamp ' + str(partialTime[i] + minimum) + "\n|")
    print('| Performance Variation: ' + str(performanceVariation))
    print('| Transaction Troughput: ' + str(transactionTroughput))
    print('| Performance Trend: ' + str(performanceTrend))
    print('| Current State: ' + str(currentState))
    print('+-----------------------------------------------------------+\n')
    """

def plot(x, y, label, title, args, filenameAppend):
    plt.plot(x, y)
    plt.xlabel('Time (Seconds)')
    plt.ylabel(label)
    plt.title(title)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    if args.separate == 'true':
        if args.save == 'true':
            destPath = args.output_dir
            if args.output == 'false':
                destPath += args.filename.split('.')[0]
            else:
                destPath += args.output
            destPath += '_' + filenameAppend + '.png'
            print('Saving to ' + destPath)
            plt.savefig(destPath)
        else:
            plt.show()
        plt.clf()

def parseState(state):
    if (state == 'warmup'):
        return 0
    if (state == 'steady'):
        return 1
    if (state == 'under_pressure'):
        return 2
    if (state == 'stress'):
        return 3
    if (state == 'thrashing'):
        return 4
    return -1

if args.plot == 'true':
    # Subplot separates the plot window into a grid. 221 means ( 1 2 )
    # grid size is 2x2, and 1 means its on the first position: ( 3 4 )
    if args.separate != 'true':
        plt.subplot(221)
    plot(xPlot, finalPV, 'Performance Variation', 'Performance Variation x Time', args, 'pv')
    if args.separate != 'true':
        plt.subplot(222)
    plot(xPlot, finalTT, 'Transaction Troughput', 'Transaction Troughput x Time', args, 'tt')
    if args.separate != 'true':
        plt.subplot(223)
    plot(xPlot, finalPT, 'Performance Trend', 'Performance Trend x Time', args, 'pt')
    finalCS = [parseState(x) for x in finalCS]
    if args.separate != 'true':
        plt.subplot(224)
    plt.plot(xPlot, finalCS)
    plt.xlabel('Time (Seconds)')
    #plt.ylabel('Current State')
    plt.title('Current State x Time')
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,0,5))
    plt.yticks(np.arange(5), ['Warm-Up', 'Steady', 'Under\nPressure', 'Stress', 'Trashing'])

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    if args.save == 'true':
        destPath = args.output_dir
        if args.output == 'false':
            destPath += args.filename.split('.')[0]
        else:
            destPath += args.output
        if args.separate == 'true':
            destPath += '_state'
        destPath += '.png'
        print('Saving to ' + destPath)
        plt.savefig(destPath)
    else:
        plt.show()

# performanceTrend = variables.calculatePerformanceTrend(timeSorted, treatedSorted)
# print(performanceTrend)

