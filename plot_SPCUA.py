import matplotlib as mpl
mpl.use("Agg")
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import sys
from datetime import datetime, timedelta
import gc
import grayify as gfy

"""
    plot_SPCUA.py
    Author: Greg Blumberg (OU/CIMMS/SoM)
    Email: wblumberg@ou.edu

    Input:
    1.) YYYYMMDD (i.e. 20150502)
    2.) HR (i.e. 00 or 12)
    3.) LEVEL (i.e. 500)

    These inputs will allow for seaching within the current directory
    for .csv files that look like this: YYYYMMDDHH.csv

    These CSV files can be produced by the get_realtime.py script.
    
    To produce the map you will need 2 YYYYMMDDHH.csv files.  The first
    file will contain all of the observed data for the map you're making.
    The second file is the observed data from 12 hours ago.  This is needed
    to produce the tendencies.  For example, you'll need to get:
    2015021700.csv and 2015021612.csv from the get_realtime.py script.

    This script reproduces the obs-only upper air maps that
    can be seen on the SPC Upper Air page.  In the past, I've
    used the SPC maps for my own hand analyses and also to teach
    hand analyses to different students.  My version is a slight update
    in order to improve the readability of the maps by adding color to the
    map obs.  These maps provide 8 different types of data at the UA stations.

    Observations:
    1.) Upper left (black) - geopotential height in meters (truncated)
    2.) Middle left (red) - temperature in Celsius.
    3.) Lower left (green) - dewpoint in Celsius.
    4.) Winds in knots 
    
    Tendencies:
    1.) Upper right (+,red;-,blue) - geopotential height tendency (decameters)
    2.) Middle right (+,red;-,blue) - temperature tendency (Celsius)
    3.) Lower right (+,green;-,orange/brown) - dewpoint tendency (Celsius)

    Lift:
    1.) Dewpoint depression in bold at the top if TTDD <= 5 Celsius.
"""

def vec2comp(wdir, wspd):
    '''
        Underlying function that converts a vector to its components
        Parameters
        ----------
        wdir : number, masked_array
        Angle in meteorological degrees
        wspd : number, masked_array
        Magnitudes of wind vector
        Returns
        -------
        u : number, masked_array (same as input)
        U-component of the wind
        v : number, masked_array (same as input)
        V-component of the wind
    '''
    u = wspd * np.sin(np.radians(wdir % 360.)) * -1
    v = wspd * np.cos(np.radians(wdir % 360.)) * -1
    return u, v

yyyymmdd = sys.argv[1]
hr = sys.argv[2]
level = sys.argv[3]

dt = datetime.strptime(yyyymmdd+hr, '%Y%m%d%H')
dt_past = dt - timedelta(seconds=60*60*12)

cur_data = np.loadtxt(yyyymmdd+hr+'.csv', delimiter=',', dtype=str)
past_data = np.loadtxt(datetime.strftime(dt_past, '%Y%m%d%H.csv'), delimiter=',', dtype=str)

fil = np.where(np.asarray(cur_data[:,5], dtype=float) == int(level))
cur_data = cur_data[fil,:]
fil = np.where(np.asarray(past_data[:,5], dtype=float) == int(level))
past_data = past_data[fil,:]

index_pairs = []
for i in xrange(len(cur_data[0])):
    sta = cur_data[0,i,0]
    idx = np.where(past_data[0,:,0] == sta)[0]
    if len(idx) > 0:
        index_pairs.append((i, idx[0]))
"""
# Here is where I wanted to have an option to overlay the reflectivity in light
gray al la the SPC Mesoanalysis surface observation PDF files.
# Load in the radar data if you want to
radarlink = "http://thredds.ucar.edu/thredds/dodsC/nexrad/composite/gini/n0r/1km/%Y%m%d/Level3_Composite_n0r_1km_%Y%m%d_%H%M.gini"
radar_dat = Dataset(datetime.strftime(dt, radarlink))
stride = 30
ref = radar_dat.variables['Reflectivity'][0,::stride,::stride]
ref_grid = np.load('1kmref_grid.npz')
ref_grid_lat = ref_grid['lat'][::stride,::stride]
ref_grid_lon = ref_grid['lon'][::stride,::stride]
"""

plt.figure(figsize=(17,11))
m = Basemap(llcrnrlon=-120,llcrnrlat=20,urcrnrlat=50, urcrnrlon=-55,
            resolution='h',projection='stere',\
            lat_ts=50,lat_0=50,lon_0=-97., area_thresh=10000)
m.drawcoastlines(color='#999999')
m.drawcountries(color='#999999')
m.drawstates(color='#999999')
m.drawparallels(np.arange(-80.,81.,10.), linestyle='--', alpha=.5, color='#999999')
m.drawmeridians(np.arange(-180.,181.,10.), linestyle='--', alpha=.5, color='#999999')

"""
#Plot the radar
ref_x, ref_y = m(ref_grid_lon, ref_grid_lat)
print ref.max(), ref.min()
plt.pcolormesh(ref_x, ref_y, ref, cmap=gfy.grayify_cmap('autumn_r'), vmin=30, vmax=70)
"""

offset = 1e4
for now_idx, past_idx in index_pairs:
    gc.collect()
    cur = cur_data[0, now_idx]
    past = past_data[0, past_idx]
    lat = float(cur[2])
    lon = float(cur[3])
    x, y = m(lon, lat)
    xbnds = plt.xlim()
    ybnds = plt.ylim()
    
    if x > xbnds[1] or x < xbnds[0] or y > ybnds[1] or y < ybnds[0]:
        continue
    
    try: 
        hght = int(float(cur[8]))
    except:
        continue
    try:
        tmpc = str(round(float(cur[6]),1))
    except:
        tmpc = "M"
    try:
        dwpc = str(round(float(cur[7]),1))
    except:
        dwpc = "M"
    try:
        dewp_depr = float(tmpc) - float(dwpc)
    except:
        dewp_depr = 10

    if dewp_depr <= 5:
        plt.text(x,y+offset*8,str(int(round(dewp_depr,0))), fontweight='bold', fontsize=10, horizontalalignment='center', verticalalignment='center')
    
    left = 4
    if int(level) == 925:
        hght_string = str(hght) # Don't remove any value in any place
    elif int(level) == 850:
        hght_string = str(hght)[1:] # Remove the 1 in a 4 digit height
    elif int(level) == 700:
        hght_string = str(hght)[1:]
    elif int(level) == 500:
        hght_string = str(hght)[:3]
    elif int(level) == 300:
        hght_string = str(hght)[:3]
    elif int(level) == 250:
        hght_string = str(hght)[1:4]
    else:
        print "THIS LEVEL IS NOT YET SUPPORTED IN THE PROGRAM."
        sys.exit()

    print "PLOTTING OBS..."
    plt.text(x-left*offset,y+offset*4,hght_string, fontsize=9, horizontalalignment='right', verticalalignment='center', color='k')
    plt.text(x-left*offset,y,tmpc, fontsize=9, horizontalalignment='right', verticalalignment='center', color='r')
    plt.text(x-left*offset,y-offset*4,dwpc, fontsize=9, horizontalalignment='right', verticalalignment='center', color='g')
    
    print "PLOTTING TENDENCIES..."
    right = 6
    try:
        string = str(int(round(float(hght) - float(past[8]),0)/10))
    except:
        string = "M"
    if string == "M" or string == '0':
        color='k'
    elif int(string) > 0:
        color='r'
    else:
        color='b'

    plt.text(x+right*offset,y+offset*4,string, fontsize=9, horizontalalignment='right', verticalalignment='center', color=color)
    try:
        string = str(int(round(float(tmpc) - float(past[6]),0)))
    except:
        string = "M"
    
    if string == "M" or string == '0':
        color='k'
    elif int(string) > 0:
        color='r'
    else:
        color='b'
    
    plt.text(x+right*offset,y,string, fontsize=9, horizontalalignment='right', verticalalignment='center', color=color)
    try:
        string = str(int(round(float(dwpc) - float(past[7]),0)))
    except:
        string = "M"
    if string == "M" or string == '0':
        color='k'
    elif int(string) > 0:
        color='g'
    else:
        color='#CC6600'
   
    plt.text(x+right*offset,y-offset*4,string, fontsize=9, horizontalalignment='right', verticalalignment='center', color=color)
    
    print "PLOTTING WINDS..."
    try:
        wdir = float(cur[9])
        wspd = float(cur[10])
        u, v = vec2comp(wdir, wspd)
        u_map, v_map = m.rotate_vector(np.asarray([[u]]), np.asarray([[v]]), np.asarray([[lon]]), np.asarray([[lat]]))
        m.barbs(x,y, u_map[0][0],v_map[0][0], length=8, sizes={'spacing':.15,'width':.15,'height':.35,'emptybarb':.001})
    except:
        print "UNABLE TO PLOT WINDS."
    
map_details_x, map_details_y = m(-95,24) 
plt.text(map_details_x, map_details_y, str(level) + ' mb ' + datetime.strftime(dt, "%Y%m%d/%H%M"), fontsize=18, fontweight='bold', fontstyle='italic') 
plt.tight_layout()
plt.savefig(datetime.strftime(dt, '%Y%m%d_%H_') + str(int(level)) + '.pdf',bbox_inches='tight', pad_inches=0)


