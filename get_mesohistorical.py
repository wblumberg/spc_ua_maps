import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import tz
import matplotlib.dates as dts
import urllib
import random
import sys
from StringIO import StringIO

'''
    get_mesohistorical.py
    Author: Greg Blumberg (OU/CIMMS/SoM)
    Email: wblumberg@ou.edu

    This script will grab UA historical data from the AGWEATHER archive
    and parse it into the CSV file needed to plot it via the plot_SPCUA.py
    script.

    Archive path: http://agweather.mesonet.org/data/public/noaa/upperair/mdf/

    Inputs:
    1.) yyyymmdd (i.e. 19740403)
    2.) hr (i.e. 12 or 00)
'''

yyyymmdd = sys.argv[1]
hr = sys.argv[2]

def get_url(dt):
    
    #Load in the data for these times and append to the heights
    #Times needs to be a list of datetime objects
    RMISSD = '--'
    #Code for incrementing across each 
    url = 'http://agweather.mesonet.org/data/public/noaa/upperair/mdf/%Y/%m/%d/%Y%m%d%H%M.mdf' 
    url = datetime.strftime(dt, url) 
    return url

def readData(url):
    print "READING URL" 
    try:
        snfile = urllib.urlopen(url).read()
    except:
        print "CANNOT READ:", url
        sys.exit()
    sound_data = StringIO( snfile )
    data = np.genfromtxt( sound_data, dtype=str, skiprows=2)
    return data

sndata = readData(get_url(datetime.strptime(yyyymmdd+hr, '%Y%m%d%H')))

n = open(yyyymmdd+hr+'.csv', 'w')
for i in range(1,len(sndata)):
    station = sndata[i,0]
    wmoid = sndata[i,1]
    lat = sndata[i,3]
    lon = sndata[i,4]
    elev = sndata[i,5]
    pres = sndata[i,7:17]# index 7 = 1000 mb pres 
    temp = np.where(np.asarray(sndata[i,19:29], dtype=float) <= -991.0, '--', sndata[i,19:29])
    dwpc = np.where(np.asarray(sndata[i,31:41], dtype=float) <= -991.0, '--', sndata[i,31:41])
    wdir = np.where(np.asarray(sndata[i,43:53], dtype=float) <= -991.0, '--', sndata[i,43:53])
    wspd = np.where(np.asarray(sndata[i,55:65], dtype=float) <= -991.0, '--', sndata[i,55:65])
    hght = np.where(np.asarray(sndata[i,67:77], dtype=float) <= -991.0, '--', sndata[i,67:77])
    for j in range(len(hght)):
        string = ','.join([wmoid, station, lat, lon, elev, pres[j], temp[j], dwpc[j], hght[j], wspd[j], wdir[j]])
        print string
        n.write(string + '\n')
n.close()


