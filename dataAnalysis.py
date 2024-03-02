import json
import matplotlib
from datetime import datetime, timedelta
import numpy
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2

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

city = "Guelph"





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



options = ["humidity","temperature","pressure","dewPoint","windSpeed"]
mode = ["polyfit","scatter"]

for option in options:
    x = []
    y = []
    for elem in sortedMain:
        x.append( mdates.date2num(elem["PredictionDateTime"]))
        y.append(elem[option])


    plt.figure(figsize=(8, 6))
    plt.xlabel('Prediction Date')
    plt.ylabel(option)

    plt.title('Polyfit Plot of ' + option)
    mymodel = numpy.poly1d(numpy.polyfit(x, y, 10))
    myline = numpy.linspace(min(x), max(x), 10)
    plt.scatter(x, y)
    plt.plot(myline, mymodel(myline))
    plt.savefig("assets/plots/" + mode[0] + "/2024-02-22_to_date" + option + '.png')
    
    plt.cla()
    
    plt.title('Scatter Plot of ' + option)
    plt.scatter(x, y)
    plt.savefig("assets/plots/" + mode[1] + "/2024-02-22_to_date" + option + '.png')

print("today is "+ str(datetime.date(datetime.now())))

for elem in sortedFutures:
    date_format = "%Y_%a_%d_%b"
    # Convert the string to a datetime object
    # TODO change the year set to strip from year querried to prevent data aging errors, also account for new years

    # we assign the year ahead of time because time strp will error if you strp feb 29 from a non leap year
    day = "2024_" + elem["Date"]
    date_object = datetime.date(datetime.strptime(day, date_format))
    print(date_object)
    if date_object == datetime.date(datetime.now()):
        print("yes")