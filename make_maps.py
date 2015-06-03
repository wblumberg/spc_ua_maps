import os
from datetime import datetime, timedelta

levels = [925,850,700,500,300,200]
times = [00, 12]

dt = datetime.utcnow()

python = '/data/soundings/anaconda/bin/python'
realtime_path = '/data/soundings/blumberg/programs/spc_ua_maps/get_realtime.py'
command = python + ' ' + realtime_path + " "

if dt.hour < 12:
    print command
    os.system(command + datetime.strftime(dt, "%Y%m%d 00"))
    os.system(command + datetime.strftime(dt - timedelta(seconds=60*60*24), "%Y%m%d 12"))
    map_hour = '00'
    print map_hour
else:
    print command
    os.system(command + datetime.strftime(dt, "%Y%m%d 12"))
    os.system(command + datetime.strftime(dt, "%Y%m%d 00"))
    map_hour = '12'

for l in levels:
    command = python + ' /data/soundings/blumberg/programs/spc_ua_maps/plot_SPCUA.py ' + datetime.strftime(dt, '%Y%m%d ') + map_hour + ' ' + str(l)
    print command
    os.system(command)

os.system('/usr/bin/rm /data/soundings/blumberg/programs/spc_ua_maps/*.csv')

os.system('/usr/bin/mv /data/soundings/blumberg/programs/spc_ua_maps/*.pdf /data/soundings/blumberg/programs/spc_ua_maps/maps/')
days = 5
old_dt = dt - timedelta(seconds = 60*60*24*days)

command = '/usr/bin/rm /data/soundings/blumberg/programs/spc_ua_maps/maps/' + datetime.strftime(old_dt, '%Y%m%d*.pdf')
print command
os.system(command)

