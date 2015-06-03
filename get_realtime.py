from subprocess import call
import numpy as np
from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date
import glob
import sys
import os

"""
    get_realtime.py
    Author: Greg Blumberg (OU/CIMMS/SoM)
    Email: wblumberg@ou.edu

    This script downloads the needed upper air data and put it
    into the needed CSV files produce the colorized SPC UA plots.
    The data comes from the unidata2.new.ssec.wisc.edu link and 
    is downloaded by WGET.  You'll need WGET to run this script.

    Inputs:
    1.) YYYYMMDD (i.e. 20150217)
    2.) HR (i.e. 12 or 00)
"""

yyyymmdd = sys.argv[1]
hr = sys.argv[2]

link = 'http://unidata2-new.ssec.wisc.edu/decoded/netcdf/upperair/Upperair_%Y%m%d_0000.nc'

link = link.replace('%Y%m%d', yyyymmdd)
call(['wget', '--directory-prefix=/data/soundings/blumberg/programs/spc_ua_maps/', link])

units = 'seconds since 1970-01-01 00:00:00+00:00'

now_dataset = Dataset('/data/soundings/blumberg/programs/spc_ua_maps/' + link.split('/')[-1])
now_dts = num2date(now_dataset.variables['synTime'][:], units)
print now_dataset.variables.keys()
now_stations = []
for s in now_dataset.variables['staName'][:]:
    now_stations.append(''.join(s))

dt = datetime.strptime(yyyymmdd+hr, '%Y%m%d%H')
idx = np.where(now_dts == dt)[0]

lat = now_dataset.variables['staLat'][idx]
lon = now_dataset.variables['staLon'][idx]
alt = now_dataset.variables['staElev'][idx]
wmoID = now_dataset.variables['wmoStaNum'][idx]
presMand = now_dataset.variables['prMan'][idx,:]
tmpcMand = now_dataset.variables['tpMan'][idx,:] - 273.15
dwpcMand = -1. * (now_dataset.variables['tdMan'][idx,:] - tmpcMand)
hghtMand = now_dataset.variables['htMan'][idx,:]
wspdMand = now_dataset.variables['wsMan'][idx,:] * 1.94384
wdirMand = now_dataset.variables['wdMan'][idx,:]
now_stations = np.asarray(now_stations)[idx]
now_stations = np.where(now_stations == '', '--', now_stations)

out = open('/data/soundings/blumberg/programs/spc_ua_maps/'+yyyymmdd+hr + '.csv', 'w')
for i, sta in enumerate(zip(now_stations, wmoID)):
    for l in xrange(len(presMand[i])):
        if type(presMand[i,l]) != np.ma.core.MaskedConstant:
            line = ','.join([str(sta[1]), str(sta[0]),str(lat[i]),str(lon[i]),str(alt[i]), str(presMand[i,l]), str(tmpcMand[i,l]), str(dwpcMand[i,l]), str(hghtMand[i,l]), str(wspdMand[i,l]), str(wdirMand[i,l])])
            print line
            out.write(line + '\n')
out.close()
os.system('rm /data/soundings/blumberg/programs/spc_ua_maps/*.nc')

