import json
import matplotlib

# ok so now I need to interpret this data in a meaningful way

"""
one thing I want to observe is the change in predictive measures to their average answer on the given day
so take the futures pointed at DAY and conmpare them to the average of main of that day

night temp as a future is given as a min beacause that is what people really want to know in night temps
so future:
6 days out (taken on 2024/01/01) to predict 2024/01/07
5 days out
...
1 day out
day of 2024/01/07 5pm - 11pm + 2024/01/08 12am - 5am
give a plot of 
|actual - future / actual|*100 <- percent error
|actual - future| <- abs error

this is a low level comparrison

next we want to compare these graphs over a week or month to give prediction of error 

then when supplied with todays predition of ex: 2 days away -> calculate this value into a range and do it for all predictions
"""



