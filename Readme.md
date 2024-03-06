# Python Weather Data Scraper and Visualizer

This repository hosts a major Python project aimed at extending Python's functionality into data storing, querying, and live data visualization using Matplotlib to showcase mathematical skills.

The project leverages GitHub Actions extensively for automation.

## Overview

The program retrieves raw HTML from [Environment and Climate Change Canada](https://www.weather.gc.ca) and scrapes through it for links to subpages containing weather data for approximately 170 cities. It then utilizes various regex functions to extract useful weather information for each city, which is subsequently stored in a standardized JSON document format.

The choice of JSON document storage serves two primary purposes:
1. It supports documentDB-style storage.
2. It allows for the potential expansion of scrape programs tailored to different regions, creating a standard document that remains compatible with the data display program. This separation of data collection from data presentation enhances flexibility.

The script is embedded into GitHub Actions to execute the scraping process once every hour on a Linux virtual machine. The generated JSON files are committed to this repository. A secondary script processes the weather information and generates statistical representations using Matplotlib.

Recent.json acts as a dictonary pointer connecting the city name to the most recent file data for that city for API access

## [Data Rights](https://weather.gc.ca/mainmenu/disclaimer_e.html)

If this link is not operational please check [dataLicense.txt](https://github.com/Leosly7663/Weather-Data-Analysis/blob/main/dataLicense.md)

## Contribute
This project is open source under the Apache 2.0 license feel free to clone this repo for your own uses or learning. I am also open to any bug fixes or modifications, please open a PR and leave a small note about what your changes fixes <3

For more details on how to run Python scripts using GitHub Actions, refer to [this guide](https://www.python-engineer.com/posts/run-python-github-actions/).


