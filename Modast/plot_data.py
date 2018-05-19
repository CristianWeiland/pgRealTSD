# Libraries
import json
import time
import argparse
import matplotlib.pyplot as plt
from pprint import pprint

# Local Imports
import variables # ./variables.py
import states # ./states.py

parser = argparse.ArgumentParser(description='Plot Number of Requested / Treated Transactions x Time.')

parser.add_argument('-f', '--filename', action="store", dest="filename",
            help="[str] name of the JSON file containing data. Default = data.json.", default="data.json")
parser.add_argument('-nt', '--normalize', action="store", dest="normalize",
            help="[str true/false], if we should or not normalize time. Default = true.", default="true")

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
minimum = 0
if args.normalize == 'true':
    minimum = timeSorted[0] - 1 # -1 to make sure we wont have 0 seconds as time
    timeSorted = [x - minimum for x in timeSorted]

plt.plot(timeSorted, requestedSorted)
plt.plot(timeSorted, treatedSorted)
plt.legend(['# of Requested Transactions', '# of Treated Transactions'], loc='upper right')
plt.xlabel('Time (Seconds)')
plt.ylabel('Number of Transactions')
plt.title('Treated / Requested Transactions x Time (seconds)')

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()

