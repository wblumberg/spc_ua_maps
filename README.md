#Colorized SPC Upper Air Maps

Author: Greg Blumberg (OU/CIMMS/SoM)

Email: wblumberg@ou.edu

---------------------------------------------------------------------------

This repository contains code that can be used to recreate the SPC UA maps
using Matplotlib's Basemap code.  I decided to recreate these maps after being
frustrated with the inabilty to see the numbers at each station well and also
unable to retrieve archived unanalyzed UA maps.  In order to improve the maps,
I decided to make them in color in order to make the values easier to identify
and easier to identify trends as one of my favorite parts of the original maps
were the existance of the height/temperature/dewpoint 12-hour tendencies and
the dewpoint depression information.

This codebase contains two primary scripts:

get_realtime.py - a script to pull the UA data from the Motherlode UCAR data source and dump it into a CSV file.

plot_SPCUA.py - a script that will read 2 CSV files and construct the map based on a user specified pressure level.

    These maps provide 8 different types of data at the UA stations.
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
    1.) Dewpoint depression in bold at the top if the dewpoint depression <= 5 Celsius.
