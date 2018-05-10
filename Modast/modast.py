import json
import variables
from pprint import pprint

# TODO: Have default filename and check if we have a parameter from command line args
with open('data.json') as f:
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
# TODO: Parametrizar se fazemos isto ou não isto
minimum = timeSorted[0]
timeSorted = [x - minimum for x in timeSorted]

performanceTrend = variables.calculatePerformanceTrend(timeSorted, treatedSorted)

print(performanceTrend)

