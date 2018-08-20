import csv, json
from geojson import Feature, FeatureCollection, Point, LineString
import geopandas as gpd
import geojsonio
import os

# read csv file, and create GeoJSON Feature
features = []
with open(os.path.join("data", "plane_data_fixed.csv"), newline = '') as cfile:
    rd = csv.reader(cfile, delimiter =',')
    for org_lat, org_long, dest_lat, dest_long, ignore in rd:
        org_lat, org_long = map(float, (org_lat, org_long))
        dest_lat, dest_long = map(float, (dest_lat, dest_long))
        features.append(
            Feature(
                geometry = LineString([(org_long, org_lat), (dest_long, dest_lat)])
            )
        )

# write Feature to GeoJSON file
collection = FeatureCollection(features)
with open("target_file.geojson", "w") as f:
    f.write('%s' % collection)

lines = gpd.read_file('target_file.geojson')
lines = lines.to_json()

# display geojson to broweser io
geojsonio.display(lines)
