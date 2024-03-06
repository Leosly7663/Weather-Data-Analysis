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
            if(loop in {5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34}):
                if(re.match("^", string)): 
                    # alright hear me out here
                    # the files are always formatted the same way and who tf is updating weather.gc.ca 
                    # so its not the worst idea to just pick out what I want instead of making a horribly complicated regex filter
                    # I'm a full time student so cherry picking our info is how we're doing it <3
                    if (loop == 16 and string != "Tendency:"):
                        mainForecast.append("x")
                        mainForecast.append("not recorded at source")
                        mainForecast.append(string)
                    else:
                        mainForecast.append(string)
                

    loop = 0

    


    for i in range(7):
        elements = soup.find_all(class_="div-column")[i]
        for element in elements:
            for string in element.stripped_strings:
                # Check if the string matches the regex pattern
                loop += 1
                
                if re.match("^(?!\\*)", string):
                    futureForecast[i].append(string)
        

    #['Sat', '3', 'Feb', '1', '°', 'C', 'Mainly sunny', 'Night', '-13', '°', 'C', 'A few clouds']  
  
if onlineValidate():
    cityLinks = []
    cityNames = []
    scrapeCity(cityNames, cityLinks)


    #for cityLink in cityLinks:
    for x in range(len(cityLinks)):
            
        mainForecast = []
        futureForecast = [[],[],[],[],[],[],[]]
        cityLink = cityLinks[x]
        scrapeWeather(cityLink,mainForecast,futureForecast)

        try:
            observedAt = mainForecast[1] + " " + mainForecast[2] + " " + mainForecast[3]
            condition = mainForecast[5]
            tendency = mainForecast[10]
            windDir = mainForecast[20] 
        


            def TypeCastInt(x):
                temp = []
                try:
                    for elem in mainForecast[x]:
                        if elem.isnumeric() or elem == "-":
                            temp.append(elem)
                    
                    var = "".join(temp)
                    return int(var)
                except ValueError:
                    return None
                
            def TypeCastFlt(x):
                temp = []
                try:
                    for elem in mainForecast[x]:
                        # will make a whitelist if there is another filter condition
                        if elem.isnumeric() or elem == "." or elem == "-":
                            temp.append(elem)
                    
                    var = "".join(temp)
                    return float(var)
                except ValueError:
                    return None


            Main = {
                "dateQueried": str(dateQueried),
                "timeQueried": str(timeQueried),
                "observedLocation": observedAt,
                "condition": condition,
                "pressure": TypeCastFlt(7),
                "tendency": tendency,
                "temperature": TypeCastFlt(12),
                "dewPoint": TypeCastFlt(15),
                "humidity": TypeCastFlt(18),
                "windDirection": windDir,
                "windSpeed": TypeCastInt(21)
            }
        
        except IndexError:
            Main = {"error":"No data collected for " + cityNames[x] + ". Error source upstream, consult weather data provider for details"}

        json_object_main = json.dumps(Main, indent=4)

        # Writing to sample.json
        with open("Assets/Data/"+cityNames[x]+"/Main_" + str(dateQueried) + "_Queried_at_" + str(timeQueried)+".json", "w") as outfile:
            print("Stored main data to " + str(outfile),file=logs)
            outfile.write(json_object_main)

            outfileAsStr = "Assets/Data/"+cityNames[x]+"/Main_" + str(dateQueried) + "_Queried_at_" + str(timeQueried)+".json"


            def read_json_file(filename):
                with open(filename, 'r') as file:
                    data = json.load(file)
                return data

            def write_json_file(data, filename):
                with open(filename, 'w') as file:
                    json.dump(data, file, indent=4)

            filename = "Assets/Recent.json"

            # Read JSON data from file
            json_data = read_json_file(filename)

            # Modify the dictionary as needed
            json_data[cityNames[x]] = outfileAsStr

            # Write the modified dictionary back to the file
            write_json_file(json_data, filename)

        # strip one row of future conditions
        tonightText = futureForecast[0][0]
        if tonightText == "Tonight":
            # skip futures scrape
            continue
        else:
            for i in range(0,6):
                j = 0
                tonightText = futureForecast[i][0] + "_" + futureForecast[i][1] + "_" + futureForecast[i][2]
                try:
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

                except IndexError:
                    # Stops scraping of futures when there is less info to be scraped so we dont overwrite with the tonight data that SUCKS
                    continue

           

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

        ['Observed at:', 'Moose Creek Wells', '7:00 PM', 'EST', 'Condition:', 'Not observed', 'Pressure:', '102.6', 'kPa', 'Tendency:', 'Rising', 'Temperature:', '0.8°', 'C', 'Dew point:', '0.3°', 'C', 'Humidity:', '97%', 'Wind:', 'calm', '1°', 'C', 'Condition:', 'Not observed', 'Pressure:', '102.6', 'kPa']

        """


        


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



        
print("Operation Success",file=logs)