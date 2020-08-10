#Internet speedtest usefull to check local speed network 
# Use source code from https://github.com/sivel/speedtest-cli
#Author script: Juan David Duque 
#Date created 9 august 2020

from internet_functions import animate,csv_read
import os
import datetime

begin_time = datetime.datetime.now()
animate()
print("Execution time is : " , datetime.datetime.now() - begin_time)
csv_read()


#remove file to avoid trash 
os.remove('internet_speeds_dataset.csv')