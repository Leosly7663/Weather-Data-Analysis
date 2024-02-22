import json
import matplotlib
from datetime import datetime, timedelta

# ok so now I need to interpret this data in a meaningful way

"""
one thing I want to observe is the change in predictive measures to their average answer on the given day
so take the futures pointed at DAY and compare them to the average of main of that day

night temp as a future is given as a min because that is what people really want to know in night temps
so future:
6 days out (taken on 2024/01/01) to predict 2024/01/07
5 days out
...
1 day out
day of 2024/01/07 5pm - 11pm + 2024/01/08 12am - 5am
give a plot of 
|actual - future / actual|*100 <- percent error
|actual - future| <- abs error

this is a low level comparison

next we want to compare these graphs over a week or month to give prediction of error 

then when supplied with todays prediction of ex: 2 days away -> calculate this value into a range and do it for all predictions
"""

city = "Barrie"





import os
import re


current_dir = os.path.dirname(__file__)

futures = []
main = []

# Get the list of files in the directory
files = os.listdir(current_dir+ "/Assets/Data/" + str(city))

# Iterate over the files using a for loop
for file_name in files:
    # Do whatever you want with each file
    
    dataStream = open("Assets/Data/" + str(city) +"/"+ str(file_name), "r")
    json_data = json.load(dataStream)

    if re.search(r'Future', file_name):
        futures.append(json_data)

    elif re.search(r'Main', file_name):
        main.append(json_data)

for weather in futures:
    dateString = weather["dateQueried"]
    
    date = datetime.strptime(dateString, '%Y-%m-%d').date()

    delta = timedelta(days= weather["DaysFromMain"])

    predictionDate = date + delta



    # we add this date locally to save DB space and JSON does not support date types
    weather["PredictionDate"] = predictionDate

# sort this by the date being predicted
sortedFutures = sorted(futures, key=lambda x: x['PredictionDate'])

# to be able to move into prediction comparison we will have to wait for the DB to cook a little so we have enough data to work with but lets do some stuff with main for now

for weather in main:
    dateString = weather["dateQueried"]
    
    date = datetime.strptime(dateString, '%Y-%m-%d').date()

    timeString = weather["timeQueried"]
    
    time = datetime.strptime(timeString, '%Hh%Mm').time()


    # we add this date locally to save DB space and JSON does not support date types
    weather["PredictionDateTime"] = datetime.combine(date, time) + timedelta(days=1)


sortedMain = sorted(main, key=lambda x: x['PredictionDateTime'])
# now we are organized as most recent prediction
sortedMain.reverse()

x = []
y = []

for elem in sortedMain:
    x.append(elem["PredictionDateTime"])
    y.append(elem["temperature"])

import numpy
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

x = mdates.date2num(x)

mymodel = numpy.poly1d(numpy.polyfit(x, y, 8))

myline = numpy.linspace(min(x), max(x), 10)

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show()

