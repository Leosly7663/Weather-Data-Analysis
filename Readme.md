## This is a major Python project
The goal of this project is to extend my python functionality into data storing and quering and using live data (1 hour rescrape) in matplotlib to show off math skills 

TODO:
going to integrate the auto webscrape script into github actions to allow me to move the automation off my local machine, this could also be achieved by AWS EC2 but I'm not rich so thats not happening, sane reason this program relies off python-mysql instead of Flask because I do not want to pay for cloud compute :)
https://www.python-engineer.com/posts/run-python-github-actions/ 

add status updates through actions to PM me if there are errors in the .py script, AWS manages any error with RDS

totally could have set up an event listener to monitor changes on weather.gc.ca to only run this when the data changes and make snapshots from there
didnt consider that when making this an the 1 hour timer is functionally the same for our purposes
may change this functionality in the future
