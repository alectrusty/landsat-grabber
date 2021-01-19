# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 2020

Request and pull LandSat 8 satellite imagery

@author: ATrusty
"""

import re
import geopandas as gpd
import pandas as pd
import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer

# set user parameters
username = 'atrusty'
password = ''  # enter Earth Explorer Password
aoi_path = ""  # enter path to AOI shapefile
tar_dir = ""  # enter path to write out TAR files
skip = r'804403'    # add a string to search and skip if there is a path/row you'd like to ignore
DOWNLOAD = True     # set to 'True' if you wish to proceed with download, 'False' if you wish to review scenes

# get bounds of provided aoi shapefile
aoi = gpd.GeoDataFrame.from_file(aoi_path)
aoi = aoi.to_crs('epsg:4326')  # convert to WGS for decimal coordinates
bounds = aoi.head().bounds

# build a list of longs and lats to iterate over
longs = [float(bounds['minx']), float(bounds['maxx'])]
lats = [float(bounds['miny']), float(bounds['maxy'])]
longs = longs[1:] # [0:1] for 32, [1:0] for 31
lats = lats[1:]

# search and download imagery for lower left and upper right bounds
for i in range(len(longs)):
    # initialize a new API instance and get an access key
    api = landsatxplore.api.API(username, password)
    print("Searching scenes from longitude: {}, latitude: {} ....".format(longs[i], lats[i]))

    # Request
    scenes = api.search(
        dataset='LANDSAT_8_C1',
        latitude=lats[i],
        longitude=longs[i],
        start_date='2018-03-01',
        end_date='2018-03-05',
        max_cloud_cover=100)

    print('{} scenes found.'.format(len(scenes)))
    api.logout()

    # download cloudless scenes
    if DOWNLOAD:
        for scene in scenes:
            ee = EarthExplorer(username, password)

            if re.search(skip, scene['entityId']):
                print('Skipping scene: {} ....'.format(scene['entityId']))
            else:
                print('Downloading scene: {} ....'.format(scene['entityId']))
                ee.download(scene_id=scene['entityId'], output_dir=tar_dir)

            ee.logout()
    else:
        for scene in scenes:
            print(scene['entityId'])

