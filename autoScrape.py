# pip install urllib
import urllib
import urllib.error
from urllib.request import Request, urlopen
import urllib.request
import re
import requests
import datetime
import json
import os 

dateQueried = datetime.date.today()
timeQueried = datetime.datetime.now()
timeQueried = timeQueried.strftime("%Hh%Mm")

logs = open("Logs/" + str(dateQueried) + "_logged_at_" + str(timeQueried)+".txt", "w")

# pip install beautifulsoup4
from bs4 import BeautifulSoup, SoupStrainer

def onlineValidate():
    try:
        internetCheck = urllib.request.urlopen('https://www.youtube.com/')
    except urllib.error.URLError:
        print("Internet connection failed please check network connection settings",file=logs)
        return False
    else:
        if str(internetCheck.getcode()) == "200":
            print("Internet connection successful",file=logs)
            return True
        print("Url request failed - reason unknown",file=logs)
        return False
        

def scrapeCity(cityNames, cityLinks):
    # sends a request to the website then returns the HTML infor to be sorted for usable info
    weatherReq = Request('https://weather.gc.ca/forecast/canada/index_e.html?id=ON', headers={'User-Agent': 'Mozilla/5.0'})
    weatherDoc = urlopen(weatherReq).read()
    print("Connected to weather source",file=logs)

    soup = BeautifulSoup(weatherDoc, 'html.parser')
        # by giving it a class to look for you can get the specific information you need much easier
    for i in range(3):
        soupText = soup.find_all(class_="list-unstyled col-sm-4")[i]
        for element in soupText:
            if element != "\n":
                cityNames.append(element.get_text())
        for link in soupText.find_all('a', href=True):
            cityLinks.append("https://weather.gc.ca/" + link['href'])

        # we have scraped the foundational information for the selection menu presenting you with where you want to get the weather info from
                
        # In a production env this will be modularized, and its output routed to a file store where the main program will call on instead of having to rescrape every second

def scrapeWeather(links, mainForecast, futureForecast):

     # sends a request to the website then returns the HTML infor to be sorted for usable info
    weatherReq = Request(links, headers={'User-Agent': 'Mozilla/5.0'})
    weatherDoc = urlopen(weatherReq).read()


    soup = BeautifulSoup(weatherDoc, 'html.parser')
        # by giving it a class to look for you can get the specific information you need much easier

    elements = soup.find_all(class_="hidden-xs row no-gutters")
    loop = 0

    # Iterate through elements and filter strings
    for element in elements:
        # Iterate through the strings of the element
        for string in element.stripped_strings:
            # Check if the string matches the regex pattern
            loop += 1
            if re.match("^", string): 
                # alright hear me out here
                # the files are always formatted the same way and who tf is updating weather.gc.ca 
                # so its not the worst idea to just pick out what I want instead of making a horribly complicated regex filter
                # if you've dug this deep into my code to review it, you obv know what you're doing and we both know theres a better way to do this
                # but im not getting paid for this and I'm a full time student so cherry picking our info is how we're doing it <3
                if loop in {5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34}:
                    mainForecast.append(string)

    loop = 0

    


    for i in range(7):
        elements = soup.find_all(class_="div-column")[i]
        for element in elements:
            for string in element.stripped_strings:
                # Check if the string matches the regex pattern
                loop += 1
                if re.match("^", string): 
                    futureForecast[i].append(string)
        

    #['Sat', '3', 'Feb', '1', '°', 'C', 'Mainly sunny', 'Night', '-13', '°', 'C', 'A few clouds']  
  
if onlineValidate():
    cityLinks = []
    cityNames = []
    scrapeCity(cityNames, cityLinks)
    mainForecast = []
    futureForecast = [[],[],[],[],[],[],[]]

    #for cityLink in cityLinks:
    for x in range(len(cityLinks)):
        cityLink = cityLinks[x]
        scrapeWeather(cityLink,mainForecast,futureForecast)


        """
        ['Observed at:', 'Moose Creek Wells', '11:00 AM', 'EST', 'Condition:', 'Not observed', 'Pressure:', '102.5', 'kPa', 'Tendency:', 'Rising', 'Temperature:', '-11.7°', 'C', 'Dew point:', '-18.8°', 'C', 'Humidity:', '56%', 'Wind:', 'W', '15', 'km/h', 'Wind Chill', ':', '-19', '-12°', 'C']
        [['Mon', '19', 'Feb', '-8', '°', 'C', 'Sunny', 'Tonight', '-20', '°', 'C', 'Partly cloudy'],
        ['Tue', '20', 'Feb', '-4', '°', 'C', 'A mix of sun and cloud', 'Night', '-11', '°', 'C', 'Clear'],
        ['Wed', '21', 'Feb', '3', '°', 'C', 'Sunny', 'Night', '-1', '°', 'C', '70%', 'Chance of flurries or rain showers'],
        ['Thu', '22', 'Feb', '5', '°', 'C', '60%', 'Chance of flurries or rain showers', 'Night', '0', '°', 'C', '40%', 'Chance of rain showers or flurries'],
        ['Fri', '23', 'Feb', '5', '°', 'C', '40%', 'Chance of flurries or rain showers', 'Night', '-17', '°', 'C', '40%', 'Chance of flurries'],
        ['Sat', '24', 'Feb', '-8', '°', 'C', 'A mix of sun and cloud', 'Night', '-12', '°', 'C', '60%', 'Chance of flurries'],
        ['Sun', '25', 'Feb', '-1', '°', 'C', '60%', 'Chance of flurries']]
        """




        # strip one row of future conditions
        for i in range(0,6):
            j = 0
            tonightText = futureForecast[i][0] + "_" + futureForecast[i][1] + "_" + futureForecast[i][2]
            if re.search(r"%$",futureForecast[i][6]):
                j = 1
                conditionsPassed1 = futureForecast[i][6] + " " + futureForecast[i][7]
                tempPassedNext = futureForecast[i][9]
            else:
                conditionsPassed1 = futureForecast[i][6]
                tempPassedNext = futureForecast[i][8]
            dayLabel = futureForecast[i][3]
            if re.search(r"%$",futureForecast[i][11+j]):
                conditionsPassed2 = futureForecast[i][11+j] + " " + futureForecast[i][12+j]
            else:
                conditionsPassed2 = futureForecast[i][11+j]

            Future = {
                "DaysFromMain":i,
                "Date":tonightText,
                "dayCondition":conditionsPassed1,
                "nightCondition":conditionsPassed2,
                "nightTemp":int(tempPassedNext),
                "dayTemp":int(dayLabel),
                "dateQueried":str(dateQueried),
                "timeQueried":str(timeQueried),
            }

            json_object_future = json.dumps(Future, indent=4)
        
            # Writing to sample.json
            with open("Assets/Data/"+cityNames[x]+"/Future_" + tonightText + "_Queried_at_" + str(dateQueried)+".json", "w") as outfile:
                print("Stored future data to " + str(outfile),file=logs)
                outfile.write(json_object_future)

        """
        stored every hour every day * 7
        Sub Schema 
        1                           daysFromMain                           ** second key
        Sat 24 Feb                  tonightText             Date           *
        A mix of sun and cloud      conditionsPassed1       dayCondition
        60% Chance of flurries      conditionsPassed2       nightCondition
        -12°C                       tempPassedNext          nightTemp
        -8°C                        dayLabel                dayTemp
        2/19/2024                   dateQueried             dateQueried
        11:34                       timeQueried             timeQueried
        """


        observedAt = mainForecast[1] + " " + mainForecast[2] + " " + mainForecast[3]
        condition = mainForecast[5]
        pressure = mainForecast[7]
        tendency = mainForecast[10]
        temperature = mainForecast[12]
        dewPoint = mainForecast[15]
        humdity = mainForecast[18]
        windDir = mainForecast[20] 
        windSpeed = mainForecast[21] 

        """"
        Main Schema
        2/19/2024               dateQueried                         dateQueried       *   
        print(observedAt)       Moose Creek Wells 12:00 PM EST      observedLocation  
        print(condition)        Not observed                        condition
        print(pressure)         102.5kPa                            pressure    
        print(tendency)         Rising                              tendency
        print(temperature)      -11.0°C                             temperature
        print(dewPoint)         -18.8°C                             dewPoint
        print(humdity)          53%                                 humidity
        print(windDir)          W                                   windDirection
        print(windSpeed)        14                                  windSpeed
        """

        # lets think about how we want to querry this data
        # probably by day 

        # DB is configured for traffic only from my IP so not too worried ab my password being exposed but I still hide it best I can
        """
        Deprecated MySQL :(
        mydb = mysql.connector.connect(
        host="weatherdata.cxskcu0wgqfm.us-east-1.rds.amazonaws.com",
        user="admin",
        # TODO hide this password before commit dont want that in public history
        password="",
        database="Main"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO current (name, address) VALUES (%s, %s)"
        val = ("John", "Highway 21")
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        """

        """
        Main Schema
        2/19/2024               dateQueried                         dateQueried       *   
        print(observedAt)       Moose Creek Wells 12:00 PM EST      observedLocation  
        print(condition)        Not observed                        condition
        print(pressure)         102.5kPa                            pressure    
        print(tendency)         Rising                              tendency
        print(temperature)      -11.0°C                             temperature
        print(dewPoint)         -18.8°C                             dewPoint
        print(humdity)          53%                                 humidity
        print(windDir)          W                                   windDirection
        print(windSpeed)        14                                  windSpeed
        """



        Main = {
            "dateQueried": str(dateQueried),
            "timeQueried": str(timeQueried),
            "observedLocation": observedAt,
            "condition": condition,
            "pressure": float(pressure),
            "tendency": tendency,
            "temperature": float(temperature[:-1]),
            "dewPoint": float(dewPoint[:-1]),
            "humidity": float(humdity[:-1]),
            "windDirection": windDir,
            "windSpeed": int(windSpeed)
        }

        json_object_main = json.dumps(Main, indent=4)


        # Writing to sample.json
        with open("Assets/Data/"+cityNames[x]+"/Main_" + str(dateQueried) + "_Queried_at_" + str(timeQueried)+".json", "w") as outfile:
            print("Stored main data to " + str(outfile),file=logs)
            outfile.write(json_object_main)

print("Operation Success" + str(outfile),file=logs)