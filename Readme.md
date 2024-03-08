# Python Weather Data Scraper and Visualizer

This repository hosts a major Python project aimed at extending Python's functionality into data storing, querying, and live data visualization using Matplotlib to showcase mathematical skills.

The project leverages GitHub Actions extensively for automation.

## Overview

The program retrieves raw HTML from [Environment and Climate Change Canada](https://www.weather.gc.ca) and scrapes through it for links to subpages containing weather data for approximately 170 cities. It then utilizes various regex functions to extract useful weather information for each city, which is subsequently stored in a standardized JSON document format.

The choice of JSON document storage serves two primary purposes:
1. It supports documentDB-style storage.
2. It allows for the potential expansion of scrape programs tailored to different regions, creating a standard document that remains compatible with the data display program. This separation of data collection from data presentation enhances flexibility.

The script is embedded into GitHub Actions to execute the scraping process once every hour on a Linux virtual machine. The generated JSON files are committed to this repository. A secondary script processes the weather information and generates statistical representations using Matplotlib.

Recent.json acts as a dictionary pointer connecting the city name to the most recent file data for that city for API access.

## API

You can access the data collected from this script through a Flask API endpoint at flask-apiw-eather.vercel.app/api/\<cityName\>. The information returned is a JSON documnet containing current weather data for the provided city. I have left this API publicly accessible due to the nature of the information; weather information is no secret, and I have no issue letting others use or critique my work. [Repository Link For Flask REST API](https://github.com/Leosly7663/flaskAPIWeather/tree/main)

Example: [https://flask-apiw-eather.vercel.app/api/Guelph](https://flask-apiw-eather.vercel.app/api/Guelph)

These endpoints are leveraged on my Portfolio through React.js HTTP requests to round out a full-stack application where I have build all components from the display to the API to the database and data collection

## [Data Rights](https://weather.gc.ca/mainmenu/disclaimer_e.html)

If this link is not operational, please check [dataLicense.txt](https://github.com/Leosly7663/Weather-Data-Analysis/blob/main/dataLicense.md).

## Contribute

This project is open source under the Apache 2.0 license. Feel free to clone this repo for your own uses or learning. I am also open to any bug fixes or modifications. Please open a PR and leave a small note about what your changes fix <3.

## History

For me this whole project started in 11th grade for my highschool introduction to programming class in python. There we learned TKinter for making GUI's in python, and for our final project we had been tasked with making a small python game in the GUI, I really liked my teacher for this class, he was also my physics teacher and I wanted him to like me, and like any other try hard at school I wanted to brag. So instead of making a GUI I made a HUD a transparent top layer application that would serve some form of complicated data, I did not want to just make some game either I wanted data that would be intresting on a transparent screen something that would be useful, I decieded on making the application scrape the internet every min for weather data in my city. My computer thankfully was powerful enough for this app to work running an extremely reasource intense python webscraper and GUI but I can imagine now that when my teacher ran it, it make have lit his computer on fire. and that was the first day I shipped buggy code to production and since then I've been hooked. All jokes but I do see that as the first time I made something real. Atleast for my own use, if it didn't take the processing power of NASA to run I would probably has used it a few more times. 
Now here we are almost 4 years later and I still have this cool but destructive app in my old school code, I decided I am now once again ready to try again. This next attempt was recorded in 




For more details on how to run Python scripts using GitHub Actions, refer to [this guide](https://www.python-engineer.com/posts/run-python-github-actions/).
