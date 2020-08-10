#Internet speedtest usefull to check local speed network 
# Use source code from https://github.com/sivel/speedtest-cli
#Author script: Juan David Duque 
#Date created 9 august 2020

import speedtest as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


input_times = int(input('How many time do yo want to test: '))

def get_new_speeds():
    speed_test = st.Speedtest()
    speed_test.get_best_server()

    # Get ping (miliseconds)
    ping = round(speed_test.results.ping,2)
    # Perform download and upload speed tests (bits per second)
    download = speed_test.download()
    upload = speed_test.upload()

    # Convert download and upload speeds to megabits per second
    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)
    return (ping, download_mbs, upload_mbs)



def update_csv(internet_speeds):
    # Get today's date in the form Month/Day/Year
    date_today = datetime.today().strftime("%H:%M:%S %d/%m/%Y")
    # File with the dataset
    csv_file_name = "internet_speeds_dataset.csv"

    # Load the CSV to update
    try:
        csv_dataset = pd.read_csv(csv_file_name, index_col="Date")
    # If there's an error, assume the file does not exist and create\
    # the dataset from scratch
    except:
        csv_dataset = pd.DataFrame(
            list(),
            columns=["Ping(ms)", "Download(Mb/s)", "Upload(Mb/s)"]
        )

    # Create a one-row DataFrame for the new test results
    results_df = pd.DataFrame(
        [[ internet_speeds[0], internet_speeds[1], internet_speeds[2] ]],
        columns=["Ping(ms)", "Download(Mb/s)", "Upload(Mb/s)"],
        index=[date_today]
    )
    print(results_df)

    updated_df = csv_dataset.append(results_df, sort=False)
    # https://stackoverflow.com/a/34297689/9263761
    updated_df\
        .loc[~updated_df.index.duplicated(keep="last")]\
        .to_csv(csv_file_name, index_label="Date")

plt.title("Network speed")
plt.xlabel("iterations")
plt.ylabel("Mb/s")
plt.style.use('fivethirtyeight')

#read csv file 

def csv_read():
    data = pd.read_csv("internet_speeds_dataset.csv")
    ping = data.iloc[:,1]
    download_data =  data.iloc[:,2]
    upload_data = data.iloc[:,3]  
    plot_network(ping, download_data, upload_data)
    average(download_data, upload_data)

#Plot iterations 
def plot_network(ping, download_data, upload_data):

    plt.figure(1)

    plt.subplot(3,1,1)
    plt.title("Network Speed")
    plt.plot(download_data,'r-')
    plt.legend(["Download"],loc = 'right')
       
    plt.subplot(3,1,2)
    plt.plot(upload_data,'b-')
    plt.legend(["Upload"],loc = 'right')
  
    plt.subplot(3,1,3)
    plt.plot(ping,'k-')
    plt.legend(["Ping"])
    plt.xlabel('Iterations',loc = 'right')
        
    plt.show()
    plt.tight_layout()

#Loop to create multiple file  
    
def animate():
    for count in range(input_times):
        iteration = count + 1
        print("Iteration ", iteration)
        new_speeds = get_new_speeds()
        update_csv(new_speeds)

#Compute average of iteration

def average(download_data, upload_data):
    average_download = round(sum(download_data) / len(download_data),2)
    average_upload = round(sum(upload_data) / len(upload_data),2)
    print("Average Network download speed is: ", average_download)
    print("Average Network upload speed is: ", average_upload)

animate()
csv_read()

#remove file to avoid trash 
os.remove('internet_speeds_dataset.csv')